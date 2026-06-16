import urllib.request
import json
import tkinter
import tkinter.font
from gpiozero import MotionSensor

pir_sensor = MotionSensor(14)                                                                   # GPIO 14번 핀에 연결된 인체 감지 센서 객체를 생성합니다.
API_KEY = "Enter your API key here"                                                             # 발급받은 오픈웨더맵 API 키를 입력하는 변수입니다.
is_displaying = False                                                                           # 중복 실행을 방지하기 위한 상태 관리 변수입니다.

def get_weather_data():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
        with urllib.request.urlopen(url) as r:                                                  # 오픈웨더맵 서버에 서울 지역의 날씨 데이터를 요청합니다.
            data = json.loads(r.read())
            temp = data["main"]["temp"]
            humi = data["main"]["humidity"]
            return f"현재 기온: {temp:.1f}C / 습도: {humi}%"
    except Exception:
        return "날씨 정보를 불러올 수 없습니다."

def check_motion():
    global is_displaying
    
    if pir_sensor.is_active and not is_displaying:                                              # 센서가 움직임을 감지했고 화면에 날씨가 없을 때만 실행합니다.
        is_displaying = True
        show_weather_info()
        
    window.after(500, check_motion)                                                             # 0.5초마다 이 함수를 다시 실행하여 센서 상태를 확인합니다.

def show_weather_info():
    status_label.config(text="움직임 감지! 날씨 정보를 안내합니다.", fg="red")                  # 움직임이 감지되면 상태 문구를 빨간색으로 변경합니다.
    window.update()
    
    weather_info = get_weather_data()                                                           # 대기 상태에서 보이지 않던 날씨 정보를 가져옵니다.
    weather_label.config(text=weather_info)
    
    window.after(10000, reset_standby_state)                                                    # 10초 대기 후 화면을 다시 초기 대기 상태로 복구합니다.

def reset_standby_state():
    global is_displaying
    
    weather_label.config(text="")                                                               # 날씨 정보 텍스트를 지워 화면에서 숨깁니다.
    status_label.config(text="대기 중... 움직임이 감지되면 날씨를 알려드립니다.", fg="green")   # 화면의 상태 문구를 초록색의 대기 상태로 되돌립니다.
    
    is_displaying = False                                                                       # 다시 움직임을 감지할 수 있도록 상태 변수를 초기화합니다.

window = tkinter.Tk()                                                                           # 그래픽 사용자 인터페이스 메인 창을 생성합니다.
window.title("움직임 감지 날씨 알리미")
window.geometry("500x250")
window.resizable(False, False)

title_font = tkinter.font.Font(size=16, weight="bold")                                          # 화면에 사용할 폰트 크기와 굵기를 설정합니다.
main_font = tkinter.font.Font(size=14)

title_label = tkinter.Label(window, text="움직임 감지 날씨 알리미", font=title_font)            # 화면 상단에 제목 글자를 배치합니다.
title_label.pack(pady=20)

weather_label = tkinter.Label(window, text="", font=main_font)                                  # 온습도 정보를 표시할 구역을 생성하고 배치합니다.
weather_label.pack(pady=10)

status_label = tkinter.Label(window, text="대기 중... 움직임이 감지되면 날씨를 알려드립니다.", font=main_font, fg="green") # 현재 대기 상태를 표시할 구역을 생성합니다.
status_label.pack(pady=20)

check_motion()                                                                                  # 프로그램 시작 시 센서 감시 루프를 최초로 실행합니다.

window.mainloop()                                                                               # 사용자가 창을 닫을 때까지 프로그램을 계속 실행합니다.