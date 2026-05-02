import urllib.request   # 웹 요청을 보내고 응답을 받기 위한 모듈
import json             # 웹 서버에서 받은 텍스트 데이터를 파이썬 딕셔너리로 변환하기 위한 모듈
import tkinter          # 파이썬에서 GUI를 만들기 위한 기본 라이브러리
import tkinter.font     # GUI 창 내의 텍스트 폰트와 크기를 설정하기 위한 라이브러리


API_KEY = "9d733e1d6b5f9f43ae41f94bfa0494f5"  #API 설정 (반드시 본인이 발급받은 실제 API 키를 입력해야 함)

# 날씨 정보를 가져와서 화면에 업데이트하는 함수 정의
def tick1Min():
    # OpenWeatherMap API에 서울의 날씨를 섭씨 기준으로 요청하는 URL을 생성
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric" 
    
    # URL로 요청을 보내고, 응답 결과를 'r'이라는 변수로 받음
    with urllib.request.urlopen(url) as r:
        # 받아온 데이터를 읽고, JSON 형식에서 파이썬 데이터 구조로 변환
        data = json.loads(r.read())
        
        # 변환된 데이터 중 'main' 그룹 안에 있는 'temp'(현재 온도) 값을 추출
        temp = data["main"]["temp"]
        # 변환된 데이터 중 'main' 그룹 안에 있는 'humidity'(현재 습도) 값을 추출
        humi = data["main"]["humidity"]
        
        # GUI 창에 있는 텍스트 라벨(label)의 내용을 추출한 온도와 습도 값으로 업데이트
        label.config(text=f" {temp:.1f} C {humi}%")
        
        # window(GUI 창)의 .after 메서드를 사용하여, 60,000 밀리초(즉, 1분) 뒤에 이 함수를 다시 실행하도록 예약
        # 이를 통해 1분마다 온습도 정보가 자동으로 갱신
        window.after(60000, tick1Min)

# GUI 화면(윈도우) 구성
window = tkinter.Tk()                       # 메인 GUI 창 객체를 생성
window.title("TEMP HUMI DISPLAY")           # GUI 창의 제목 표시줄 텍스트를 설정
window.geometry("400x100")                  # 창의 기본 크기를 가로 400 픽셀, 세로 100 픽셀로 설정
window.resizable(False, False)              # 사용자가 마우스로 창 크기를 임의로 조절하지 못하도록 가로, 세로 조절을 차단

# 텍스트에 적용할 폰트 속성을 설정
font = tkinter.font.Font(size=30)

# 위에서 생성한 창 내부에 글자를 표시할 라벨(Label) 위젯을 생성. 초기 텍스트는 비워두고 폰트를 적용
label = tkinter.Label(window, text="", font=font)

# 생성한 라벨 위젯을 창 안의 적절한 위치에 실제로 배치
label.pack()

# 프로그램이 시작될 때 최초로 한 번 날씨 업데이트 함수를 호출하여 화면에 바로 데이터를 띄움
tick1Min()

# GUI 창이 즉시 닫히지 않고 사용자 입력을 대기하거나 타이머 이벤트를 처리할 수 있도록 무한 루프(이벤트 대기 상태)를 실행
window.mainloop()