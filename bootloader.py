import firebase_admin
from firebase_admin import credentials, db
import os
import time
from datetime import datetime

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")  # ← 서비스 계정 키로 변경
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://rccon-1fe6f-default-rtdb.firebaseio.com/"  # ← 실제 프로젝트 ID로 바꿔주세요
})

ref = db.reference("/com/entry/")

def log_to_firebase(msg):
    print(msg)
    try:
        ref.child("log").set(msg)
    except Exception as e:
        print("[Firebase log error]", e)

def check_start():
    start_val = ref.child("start").get()

    if start_val == -1:
        print("[INFO] start=-1 detected. Shutting down Raspberry Pi...")
        log_to_firebase("[INFO] start=-1 detected. Shutting down Raspberry Pi...")
        os.system("sudo shutdown now")

    elif start_val == 1:
        print("[INFO] start=1 detected. Updating to 2 and running GPT.py...")
        log_to_firebase("[INFO] start=1 detected. Updating to 2 and running GPT.py...")
        ref.child("start").set(2)
        os.system("python3.8 GPT.py")

def kill_bootloader():
    bt = ref.child("bootloader").get()
    if bt == 0:
        log_to_firebase("[INFO] Bootloader Killed!!")
        return True
    else:
        return False

def check_prompt_change():
    prompt_change = ref.child("prompt_change").get()
    if prompt_change == 1:
        new_prompt = ref.child("prompt").get()
        with open("prompt.txt", "w") as f:
            f.write(new_prompt)
        print("[INFO] prompt.txt updated.")
        log_to_firebase("[INFO] prompt.txt updated.")
        ref.child("prompt_change").set(2)

def update_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ref.child("update").set(now)
    print(f"[INFO] Updated time: {now}")

if __name__ == "__main__":
    while True:
        try:
            check_start()
            check_prompt_change()
            update_time()
            if(kill_bootloader()):
                break
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] {e}")
            log_to_firebase(f"[ERROR] {e}")
            time.sleep(5)
