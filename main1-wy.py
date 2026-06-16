import urllib.request
import json
import tkinter
import tkinter.font
import os
import time
from gpiozero import MotionSensor

# GPIO 14번 핀에 연결된 인체 감지 센서 객체를 생성합니다.
pir_sensor = MotionSensor(14)

# 발급받은 오픈웨더맵 API 키를 입력하는 변수입니다.
API_KEY = "Enter your API key here"

def tick1Min():
    # 1분마다 오픈웨더맵 서버에 서울 지역의 날씨 데이터를 요청하여 화면을 갱신합니다.
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
            temp = data["main"]["temp"]
            humi = data["main"]["humidity"]
            weather_label.config(text=f"현재 기온: {temp:.1f}C / 습도: {humi}%")
    except Exception:
        weather_label.config(text="날씨 정보를 불러올 수 없습니다.")
    
    # 1분인 60000밀리초 후 이 함수를 다시 실행하도록 설정합니다.
    window.after(60000, tick1Min)

def handle_motion_detected():
    # 움직임이 감지되면 화면의 경고 문구를 빨간색으로 변경합니다.
    status_label.config(text="침입자 감지! 사진 촬영 진행 중...", fg="red")
    window.update()
    
    # 현재 시간을 바탕으로 사진 파일의 이름을 생성합니다.
    current_time = time.strftime("%Y%m%d_%H%M%S")
    file_path = "/home/pi/intruder_" + current_time + ".jpg"
    
    # 라즈베리파이 시스템 명령어를 호출하여 카메라 모듈로 사진을 촬영하고 저장합니다.
    os.system(f"libcamera-jpeg -o {file_path} -t 1000 --width 640 --height 480")
    
    # 촬영이 완료되면 파일 저장 경로를 화면에 파란색으로 표시합니다.
    status_label.config(text="촬영 완료 및 저장됨: " + file_path, fg="blue")
    
    # 5초 대기 후 화면을 다시 안전 상태로 복구하는 함수를 호출합니다.
    window.after(5000, reset_status_label)

def reset_status_label():
    # 화면의 문구를 초록색의 대기 상태로 되돌립니다.
    status_label.config(text="대기 상태. 움직임 감지 대기 중.", fg="green")

# 그래픽 사용자 인터페이스 메인 창을 생성합니다.
window = tkinter.Tk()
window.title("스마트홈 통합 제어 시스템")
window.geometry("450x250")
window.resizable(False, False)

# 화면에 사용할 폰트 크기와 굵기를 설정합니다.
title_font = tkinter.font.Font(size=16, weight="bold")
main_font = tkinter.font.Font(size=14)

# 화면 상단에 제목 글자를 배치합니다.
title_label = tkinter.Label(window, text="스마트홈 보안 및 기상 패널", font=title_font)
title_label.pack(pady=20)

# 온습도 정보를 표시할 구역을 생성하고 배치합니다.
weather_label = tkinter.Label(window, text="날씨 정보를 불러오는 중...", font=main_font)
weather_label.pack(pady=10)

# 인체 감지 상태를 표시할 구역을 초록색 글자로 생성하고 배치합니다.
status_label = tkinter.Label(window, text="대기 상태. 움직임 감지 대기 중.", font=main_font, fg="green")
status_label.pack(pady=20)

# 인체 감지 센서가 움직임을 인식했을 때 실행할 함수를 연결합니다.
pir_sensor.when_motion = handle_motion_detected

# 기상 정보 갱신 함수를 최초로 1회 실행하여 1분 주기의 호출을 시작합니다.
tick1Min()

# 사용자가 창을 닫을 때까지 프로그램을 계속 실행하며 대기합니다.
window.mainloop()