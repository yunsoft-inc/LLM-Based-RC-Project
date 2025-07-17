from openai import OpenAI
import serial
import time
import pyrealsense2 as rs
import numpy as np
import cv2
import base64
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import firebase_admin
from firebase_admin import credentials, db, storage
import uuid
import subprocess

# === Firebase Initialization ===
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://rccon-1fe6f-default-rtdb.firebaseio.com/",
    "storageBucket": "rccon-1fe6f.firebasestorage.app"
})

db_ref = db.reference("/com/entry/")
bucket = storage.bucket()

# === Configuration ===
api_key = os.getenv("OPENAI_API_KEY")
PORT = "/dev/ttyACM0"
BAUD = 115200
PROMPT_PATH = "prompt.txt"
RGB_PATH = "rgb.jpg"
DEPTH_PATH = "depth.png"

# === Serial Connection ===
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

# === RealSense Initialization ===
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
pipeline.start(config)

def clear_storage_folder(folder_path):
    """Firebase Storage의 특정 폴더 내 모든 파일 삭제"""
    try:
        blobs = bucket.list_blobs(prefix=folder_path)
        for blob in blobs:
            blob.delete()
        log_to_firebase(f"[Storage cleared] {folder_path}")
    except Exception as e:
        log_to_firebase(f"[Storage clear error] {e}")

def log_to_firebase(msg):
    print(msg)
    try:
        db_ref.child("log").set(msg)
    except Exception as e:
        print("[Firebase log error]", e)

def upload_to_storage(local_path, remote_filename):
    try:
        blob = bucket.blob(remote_filename)
        blob.upload_from_filename(local_path)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        log_to_firebase(f"[Upload error] {e}")
        return None

def capture_images_and_distance():
    frames = pipeline.wait_for_frames()
    color = frames.get_color_frame()
    depth = frames.get_depth_frame()
    if not color or not depth:
        return None, None, None

    color_image = np.asanyarray(color.get_data())
    depth_image = np.asanyarray(depth.get_data()).astype(np.float32)

    depth_colormap = cv2.applyColorMap(
        cv2.convertScaleAbs(depth_image, alpha=0.03),
        cv2.COLORMAP_JET
    )

    # 로컬 저장
    cv2.imwrite(RGB_PATH, color_image)
    cv2.imwrite(DEPTH_PATH, depth_colormap)

    # 기존 이미지 삭제
    clear_storage_folder("images/")

    # 새 이미지 업로드
    rgb_url = upload_to_storage(RGB_PATH, f"images/rgb_{uuid.uuid4().hex}.jpg")
    depth_url = upload_to_storage(DEPTH_PATH, f"images/depth_{uuid.uuid4().hex}.jpg")

    if rgb_url and depth_url:
        db_ref.update({
            "rgb": rgb_url,
            "depth": depth_url,
            "image_update": 1
        })

    # 거리 계산
    depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    valid_depths = depth_image[depth_image > 0]
    min_distance_m = float(np.min(valid_depths) * depth_scale) if valid_depths.size > 0 else None

    return min_distance_m, RGB_PATH, DEPTH_PATH


def read_prompt():
    """Read the user prompt from file"""
    if os.path.exists(PROMPT_PATH):
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def encode_image_base64(path):
    """Encode image to base64 string"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def ask_gpt(prompt, rgb_base64, depth_base64, closest_distance_m):
    """Send prompt and images to GPT and receive command list"""
    print("Sending request to GPT...")
    log_to_firebase("Sending request to GPT...")
    distance_info = (
        f"The closest object is approximately {closest_distance_m:.2f} meters away.\n"
        if closest_distance_m is not None else
        "Unable to determine distance to the nearest object.\n"
    )
    client = OpenAI()  # Uses your environment variable OPENAI_API_KEY
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
             "Follow Below Prompt."},
            {"role": "user", "content": [
                {"type": "text", "text": distance_info + prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{rgb_base64}"}},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{depth_base64}"}},
            ]}
        ],
        max_tokens=300
    )
    output = response.choices[0].message.content
    return output

def wait_for_done(timeout=3):
    print("Waiting for command to complete...")
    log_to_firebase("Waiting for Arduino response...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if ser.in_waiting > 0:
            result = ser.readline().decode(errors='ignore').strip()
            if result == 'E':
                log_to_firebase("Command completed.")
                return True
    log_to_firebase("Timeout: No response from Arduino.")
    return False


def execute_commands(commands):
    """Send commands to Arduino one by one"""
    for cmd in commands:
        print(f"Sending command: {cmd}")
        log_to_firebase(f"Sending command: {cmd}")
        ser.write((cmd + "\n").encode())
        wait_for_done()
        time.sleep(1) #delay

def command_processing(commands):
    commands = commands.replace('{','')
    commands = commands.replace('}','')
    temp = commands.split('|')
    rgb = temp[0]
    depth = temp[1]
    command = temp[2].replace(" ", "").split('&&')
    return rgb, depth, command
    
def execute_tts(rgb_str, depth_str):
    text = f"{rgb_str.strip()} {depth_str.strip()}"
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        log_to_firebase("ELEVENLABS API KEY error")
        return

    try:
        client = ElevenLabs(api_key=api_key)

        audio = client.text_to_speech.convert(
            text=text,
            voice_id="uyVNoMrnUku1dZyVEXwD",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        # MP3 파일로 저장
        out_path = "output.mp3"
        with open(out_path, "wb") as f:
            f.write(audio)

        # systemd에서도 동작하는 플레이어로 재생 (mpg123 권장)
        subprocess.run(["mpg123", out_path])

    except Exception as e:
        log_to_firebase(f"TTS playback failed: {e}")

def main():
    log_to_firebase("GPT RC Init...")
    try:
        while True:
            start_flag = db_ref.child("start").get()
            if start_flag == 0:
                log_to_firebase("Terminating: start == 0")
                break

            prompt = read_prompt()
            if not prompt:
                time.sleep(1)
                continue

            log_to_firebase("Capturing images...")
            distance_m, rgb_path, depth_path = capture_images_and_distance()
            log_to_firebase(f"measured distance: {distance_m}")

            if rgb_path is None:
                log_to_firebase("Failed to capture images.")
                continue

            rgb_b64 = encode_image_base64(RGB_PATH)
            depth_b64 = encode_image_base64(DEPTH_PATH)

            try:
                commands = ask_gpt(prompt, rgb_b64, depth_b64, distance_m)
            except Exception as e:
                log_to_firebase(f"GPT error: {e}")
                time.sleep(2)
                continue

            if commands:
                log_to_firebase(f"Generated commands:\n{commands}")
                if '|' not in commands:
                    log_to_firebase("Invalid commands format.")
                else:
                    rgb_str, depth_str, com_str = command_processing(commands)
                    execute_tts(rgb_str, depth_str)
                    execute_commands(com_str)
            else:
                log_to_firebase("No commands generated.")

            log_to_firebase("Waiting for next prompt...\n")
            time.sleep(2)

    except KeyboardInterrupt:
        log_to_firebase("Program terminated by user.")
    finally:
        pipeline.stop()
        ser.close()


if __name__ == "__main__":
    main()
