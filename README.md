![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=10&height=200&text=LLM%20BASED%20SELF%20DRIVING%20CAR&fontSize=40&animation=twinkling&fontAlign=40&fontAlignY=36)
# LLM 기반 자율 주행 자동차
## Hanyoung HighSchool 2025 Project

![Build Status](https://img.shields.io/badge/python-3776AB?style=flat-square&logo=html5&logoColor=000000)
![img1](https://github.com/yunsoft-inc/LLM-Based-RC-Project/blob/main/rc.png)

## 개발 동기
ChatGPT의 기술이 빠르게 발전하면서 다양한 기능들(이미지 설명, 실시간 대화 등)이 가능해졌음.
이러한 발전을 보다 보니 문득, RC카에 ChatGPT를 연동시키면 사람이 운전하듯이 자동차를 조종하는 자율 주행 자동차를 만들 수 있겠다는 생각이 들었고, 이 아이디어를 실행으로 옮기게 되었음.

## 제작에 들어간 기술들
- Python
메인 코드 작성 언어
- ChatGPT API
LLM으로 이미지 분석을 하기 위한 서비스
- ElevenLabs TTS API
음성 합성 기술
- 3D 프린팅
특수 RC카 바디 제작
- Arduino C
모터 제어, 명령 처리
- Html, JS
원격 조작 프로그램 개발
- Firebase Realtime Database, Storage, Hosting
원격 제어 서버 구축

## 프로그램에 사용된 기능들
- TTS(Text-To-Speech)
- LM(Large-Language-Model)
- 사진 촬영 및 심도 측정
- 모터 방향 및 속도 제어
- LLM 프롬프트 설계

## 작품을 개발하면서 어려웠던 점
ChatGPT에게 이미지를 인식하고 설명하도록 명령을 했더니, 사람이 감지되거나 사진에 아무 특징이 없으면 모든 형식을 무시하고 명령을 거부하는 문제가 존재했다. 이러한 문제를 해결하기 위해 검열을 피하게끔 최대한 단순하게 이미지를 설명하도록 프롬프트를 수정하고, 명령을 거부해도 출력 형식을 유지하기 위해 프롬프트를 수정했다.

고용량 배터리, 라즈베리파이, 아두이노, 스피커, 카메라를 모두 얹어서 RC카에 장착하니 무게로 인해 부하가 크게 걸려 제대로 움직이지 못하거나, 조금의 턱이 있으면 넘지를 못해 끼어버리는 문제가 있었다. 이러한 문제를 해결하기 위해 모터와 바퀴의 위치를 앞쪽으로 바꾸고, 후방에 볼캐스터를 추가 장착하여 안정성을 향상시켰다. 또한 무게중심도 안정적으로 조절하여 이동하고 정지할 때 관성으로 기우뚱거리는 문제도 해결했다.

## 작품을 만들면서 보람을 느낀점은 무엇인가?
설계한 RC카가 계획 했던대로 잘 작동하니 보람을 느꼈다.
주변 동아리 친구들에게 작품에 대한 피드백을 받으면서 내가 보완해야 할 점을 알게 되었기도 했지만, 작품을 잘 만들었다는 칭찬을 받을 때 보람을 느꼈다.

## 프로그램 개발 후 향후 진로에 미치는 영향
ChatGPT와 같은 LLM과, ElevenLabs와 같은 음성 합성 AI 모델의 무궁무진한 활용 가능성을 보았고, 컴퓨터, 전기전자, 인공지능 관련 분야로 대학 진학을 해, 관련 기술을 더 깊이 있게 배워, 더 큰 프로젝트를 진행해보고 싶다는 생각이 들었다.

## 코드 설명
1. motor.ino는 아두이노 코드 파일로 시리얼 입출력을 이용해 라즈베리파이가 모터를 조작할 수 있도록 함.
2. 라즈베리파이가 구동하는 코드는 bootloader.py와 GPT.py임.
   bootloader.py는 파이가 부팅 후 인터넷 연결이 끝나고 자동으로 실행됨. (자세한 건 아래에)
   GPT.py는 bootloader.py가 실행시키는 코드로, 실제 동작에 사용되는 코드임. (자세한 건 아래에)
3. index.html, app.js, style.css는 원격으로 제어를 편하게 하기 위해 Firebase 값들을 직관적으로 보고 실시간으로 상태를 모니터링 할 수 있도록 함.
   ![img2](https://github.com/yunsoft-inc/LLM-Based-RC-Project/blob/main/con.png)
4. prompt.txt는 GPT에게 줄 명령을 파일로 저장해 놓은 것으로 GPT.py와 같은 경로에 있어야 됨.
5. rgb, depth.png는 GPT에게 사진을 보낼 때 임시로 저장되는 이미지.

## 각 파일 별 기능 소개
GPT.py : Realsense로 사진을 찍고 rgb와 depth이미지 생성 -> 가장 가까운 거리 측정 -> 프롬프트와 사진을 GPT에게 전송 -> 받은 값을 형식에 맞게 자른 후 -> Elevenlabs api를 이용해 TTS 구현 -> 무한 반복

bootloader.py : 시작되면 서버와 5초를 주기로 통신(온라인 상태 확인) -> 서버에서 시작 명령 감지 -> GPT.py 실행 또는 서버에서 중지 명령 감지 -> GPT.py 종료

웹 서버 : 단순히 Firebase 값 조작용 UI

motor.ino : GPT.py와 통신 -> 명령 입력(EX : F,M,1) -> 모터 중간 속력으로 1만큼의 거리를 앞으로 전진 -> 완료 후 명령 이행했다는 시리얼 전송 -> 무한 반복
+ 배터리 전압, 모터 전압 실시간 확인 가능

## 전체 프로세스
1. 라즈베리파이 부팅
2. 인터넷 연결
3. bootloader.py 실행
4. 사용자 입력 대기
5. 서비스 명령 입력시 GPT.py 실행
6. 자율 주행 시작

+ 이 과정들을 웹 서버로 모니터링 가능

## 3D 모델 제작 비하인드
https://www.youtube.com/@nikodembartnik
이 분의 Open Robotics Platform 설계 사용

추가 수정 파츠 : TPU 출력이 안돼서 Petg로 출력 후 다이소 문 틈 스펀지를 붙임.
Realsense D435용 마운트 설계 및 출력
바퀴 위치 구조 변경 및 볼케스터 추가 장착

사실 이 프로젝트의 영감도 이 사람에게 받았음.
이 분의 프로젝트와 다른 점이라면, 
1. 구조 개선으로 이동 가능한 바닥이 늘었음.
2. Depth 이미지 까지 결합함으로써 장애물 회피 능력을 비약적으로 향상시킴.
3. GPT 모델의 수준이 업그레이드 됨.
4. 백엔드까지 구현을 함으로써 사용 편의성을 높임.
