# LLM-Based RC Car with GPT & Firebase
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=10&height=200&text=LLM%20BASED%20SELF%20DRIVING%20CAR&fontSize=40&animation=twinkling&fontAlign=40&fontAlignY=36)
# LLM 기반 자율 주행 자동차
## Hanyoung HighSchool 2025 Project

![Build Status](https://img.shields.io/badge/python-3776AB?style=flat-square&logo=html5&logoColor=000000)
![img1](https://github.com/yunsoft-inc/LLM-Based-RC-Project/blob/main/rc.png)

AI 기술의 발전에 따라, RC카에 ChatGPT와 TTS API를 연동하여 사람처럼 주행 명령을 이해하고, 주변을 인식하여 주행하는 자율 주행 시스템을 제작하였습니다.

---

## 📌 개발 동기

ChatGPT를 비롯한 최신 LLM 기술의 비약적인 발전을 보면서,  
"이 기술을 실제 RC카에 적용하면 사람이 명령을 내리듯 AI가 주행하지 않을까?"  
하는 아이디어에서 출발했습니다.  

단순한 라인 트레이싱을 넘어서, **자연어 명령 이해**와 **시각 정보 해석**을 통해 주행하는  
AI 기반 RC카를 직접 만들어보고 싶어 이 프로젝트를 시작했습니다.

---

## 🔧 사용된 기술 스택

| 기술 | 설명 |
|------|------|
| **Python** | 메인 프로그램 코드 작성 |
| **ChatGPT API** | LLM 기반 이미지 분석 |
| **ElevenLabs TTS API** | 음성 합성 구현 |
| **Arduino C** | 모터 및 전자 부품 제어 |
| **3D 프린팅 (PETG)** | RC카 바디 및 마운트 제작 |
| **Firebase** | 실시간 데이터베이스, 스토리지, 호스팅 |
| **HTML / JavaScript** | 원격 제어 웹 인터페이스 구현 |

---

## 🧠 구현 기능

- 📷 사진 촬영 및 심도 측정 (RealSense D435 활용)
- 💬 LLM 프롬프트 기반 이미지 설명 및 판단
- 🔊 TTS(Text-To-Speech)로 음성 출력
- ⚙️ RC카 방향/속도/거리 제어 (시리얼 명령 기반)
- 🌐 Firebase 기반 실시간 원격 제어 웹 UI

---

## ⚙️ 전체 동작 흐름

1. Raspberry Pi 부팅
2. `bootloader.py` 실행
3. Firebase 서버 상태 체크 (5초 주기)
4. 웹에서 명령 입력 시 `GPT.py` 자동 실행
5. 실시간 사진 촬영 → GPT 분석 → 음성 출력 및 RC카 주행
6. 명령 완료 시 Arduino에서 'E' 응답 → 다음 명령 실행
7. 웹에서 상태 실시간 모니터링 가능
<img src="https://github.com/yunsoft-inc/LLM-Based-RC-Project/blob/main/con.png" width="600"/>
---

## 🧩 각 파일 설명

| 파일명 | 설명 |
|--------|------|
| `motor.ino` | 아두이노 코드 - 시리얼 명령 수신 후 모터 제어 |
| `GPT.py` | 메인 로직 - 사진 촬영, GPT 요청, 음성 출력, 명령 전송 |
| `bootloader.py` | 부팅 후 Firebase 상태 체크 및 `GPT.py` 실행/종료 |
| `prompt.txt` | GPT에 전송할 기본 명령 텍스트 (동일 디렉토리에 위치 필요) |
| `rgb.png`, `depth.png` | GPT 전송용 임시 이미지 저장 파일 |
| `index.html`, `app.js`, `style.css` | Firebase UI - 명령 입력, 상태 모니터링 등 |

---

## 🔍 개발 중 어려웠던 점

### ❗ ChatGPT의 이미지 입력 문제
- 특정 조건에서 GPT가 출력 형식을 무시하고 응답을 거부하는 문제가 발생  
→ **프롬프트를 단순화**하고 **형식 유지 강제**를 통해 해결

### ❗ RC카 하중 문제
- 무거운 장비(RPi, D435, 스피커, 배터리 등) 탑재로 인한 **전진 불가/턱 끼임** 발생  
→ **무게 중심 조절, 바퀴 위치 변경, 볼캐스터 추가**로 해결

### ❗ ROS 실패 경험
- 처음엔 ROS2 + MoveIt2를 시도했으나,
  - LiDAR는 고가이고,
  - RealSense 기반 자료는 부족하여  
→ **대체 방안으로 ChatGPT 기반 주행 시스템**으로 전환

---

## ✅ 가장 보람을 느낀 점

- **설계한 대로 시스템이 잘 작동**했을 때의 성취감
- 친구들에게 작품을 소개하고 **피드백 및 칭찬**을 들었을 때의 보람
- **실제 작동하는 인공지능 로봇**을 스스로 만들었다는 자신감

---

## 🎯 진로 및 영향

- LLM, 음성 합성, IoT 시스템을 실생활에 적용해보며  
  **인공지능과 전자공학의 융합 가능성**을 직접 체험
- 이 경험을 계기로 **AI, 컴퓨터공학, 전기전자** 관련 학과 진학 목표 확립

---

## 🖼️ 3D 모델 제작 이야기

- 사용 기반 모델: [Nikodem Bartnik - Open Robotics Platform](https://www.youtube.com/@nikodembartnik)
- 변경점:
  - TPU가 출력되지 않아 **PETG로 출력**, 스펀지 패드로 충격 보완
  - **Realsense D435 마운트** 직접 설계 및 출력
  - 무게 중심 개선을 위한 **바퀴 구조 변경** 및 **볼캐스터 추가**

---

## 🚀 프로젝트 개선점 요약

| 항목 | 개선 전 | 개선 후 |
|------|---------|---------|
| 구조 안정성 | 중심이 뒤로 치우침 | 바퀴 전면 배치 + 볼캐스터 |
| 지형 대응 | 약한 장애물에도 멈춤 | 무게 중심 조절로 안정성 향상 |
| 인식 정확도 | RGB만 사용 | **RGB + Depth** 조합 |
| AI 처리 | 단순 응답 | **GPT-4 기반 지능형 판단** |
| 시스템 관리 | 수동 실행 | **Firebase 기반 원격 제어** |
