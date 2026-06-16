import urllib.request
import json
import tkinter
import tkinter.font
import os
import time
from gpiozero import MotionSensor

pir_sensor = MotionSensor(14)  # GPIO 14번 핀에 연결된 인체 감지 센서 객체를 생성합니다.


API_KEY = "Enter your API key here"       # 발급받은 API 키를 입력하는 변수입니다.

def get_weather_data():                                                                    # 오픈웨더맵 서버에 서울 지역의 날씨 데이터를 요청하여 기온과 습도 문자열을 나타냄.
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
            temp = data["main"]["temp"]
            humi = data["main"]["humidity"]
            return f"현재 기온: {temp:.1f}C / 습도: {humi}%"
    except Exception:
        return "날씨 정보를 불러올 수 없습니다."

def handle_motion_detected():
    status_label.config(text="움직임 감지! 날씨 정보를 불러오며 사진을 촬영합니다.", fg="red")    # 움직임이 감지되면 상태 문구를 갱신합니다.
    window.update()
    
    weather_info = get_weather_data()                                                      # 대기 상태에서는 보이지 않던 날씨 정보를 화면에 표시합니다.
    weather_label.config(text=weather_info)
    window.update()
    
    current_time = time.strftime("%Y%m%d_%H%M%S")                                          # 현재 시간을 바탕으로 사진 파일의 이름을 생성합니다.
    file_path = "/home/pi/motion_" + current_time + ".jpg"
    
    os.system(f"libcamera-jpeg -o {file_path} -t 1000 --width 640 --height 480")           # 라즈베리파이 시스템 명령어를 호출하여 카메라 모듈로 사진을 촬영하고 저장합니다.
    
    status_label.config(text="기록 완료: " + file_path, fg="blue")                          # 촬영이 완료되면 파일 저장 경로를 화면에 파란색으로 표시합니다.
    
    window.after(10000, reset_standby_state)                                               # 10초(10000밀리초) 대기 후 화면을 다시 초기 대기 상태로 복구하는 함수를 호출합니다.

def reset_standby_state():
    weather_label.config(text="")                                                           # 날씨 정보 텍스트를 지워 화면에서 숨깁니다.
    status_label.config(text="대기 중... 움직임이 감지되면 날씨를 알려드립니다.", fg="green")      # 화면의 상태 문구를 초록색의 대기 상태로 되돌립니다.

window = tkinter.Tk()                                                                      # 그래픽 사용자 인터페이스 메인 창을 생성합니다.
window.title("움직임 감지 날씨 알리미")
window.geometry("500x250")
window.resizable(False, False)

title_font = tkinter.font.Font(size=16, weight="bold")                                     # 화면에 사용할 폰트 크기와 굵기를 설정합니다.
main_font = tkinter.font.Font(size=14)

title_label = tkinter.Label(window, text="움직임 감지 날씨 알리미", font=title_font)          # 화면 상단에 제목 글자를 배치합니다.
title_label.pack(pady=20)

weather_label = tkinter.Label(window, text="", font=main_font)                             # 온습도 정보를 표시할 구역을 생성하고 배치합니다. 초기 상태는 빈 문자열로 설정하여 보이지 않게 합니다.
weather_label.pack(pady=10)

status_label = tkinter.Label(window, text="대기 중... 움직임이 감지되면 날씨를 알려드립니다.", font=main_font, fg="green")    # 현재 시스템의 대기 상태를 표시할 구역을 초록색 글자로 생성하고 배치합니다.
status_label.pack(pady=20)

pir_sensor.when_motion = handle_motion_detected                                            # 인체 감지 센서가 움직임을 인식했을 때 실행할 함수를 연결합니다.

window.mainloop()                                                                          # 사용자가 창을 닫을 때까지 프로그램을 계속 실행하며 대기합니다.