from gpiozero import Buzzer, DigitalInputDevice # gpiozero 라이브러리에서 부저와 디지털 입력 장치 클래스를 가져온다.
import time # 시간 지연 제어를 위한 time 라이브러리를 가져온다.

bz = Buzzer(18)              # GPIO 18번 핀을 부저 제어 객체로 초기화한다.
gas = DigitalInputDevice(17) # GPIO 17번 핀을 MQ-2 가스 센서 입력 객체로 초기화한다.

try:
    while True:                                       # 프로그램이 종료될 때까지 무한 반복하며 센서 값을 확인함.
        if gas.value == 0:    # ← 0 = 가스 감지 (LOW)  # 센서의 DO 핀 값이 0(LOW)이면 가스가 감지된 상태임.
            print("가스 감지됨")                       # 터미널 창에 가스 감지 메시지를 출력한다.
            bz.on()                                   # 부저를 켜서 위험 상황을 소리로 알림.
        else:                 # ← 1 = 정상 (HIGH)     # 센서의 값이 1(HIGH)이면 가스가 없는 정상 상태임.
            print("정상")                             # 터미널 창에 정상 메시지를 출력한다.
            bz.off()                                 # 부저를 꺼서 소리를 멈춤.

        time.sleep(0.2)                              # 0.2초 간격으로 센서 상태를 반복하여 점검한다.  

except KeyboardInterrupt:                           # 사용자가 키보드로 Ctrl + C를 입력하면 루프를 안전하게 종료한다.
    pass

bz.off()                                           # 프로그램이 종료될 때 부저가 계속 울리지 않도록 반드시 끔.
