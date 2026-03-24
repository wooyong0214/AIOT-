from gpiozero import LED    #gpiozero 라이브러리에서 'LED' 제어 클래스를 가져옵니다.
from time import sleep      # 시간 지연을 위해 'sleep' 함수를 가져옵니다.

carLedRed = 2               # 각 LED가 연결된 GPIO 핀 번호를 변수에 저장합니다. (Line 4부터 8까지)
carLedYellow = 3
carLedGreen = 4
humanLedRed = 20
humanLedGreen = 21

carLedRed = LED(2)          # 설정한 핀 번호를 사용하여 각 LED 객체를 초기화합니다
carLedYellow = LED(3)       # 또한 carLedRed, carLedYellow, carLedGreen, humanLedRed, humanLedGreen 변수에 각 핀 번호를 할당시킵니다.
carLedGreen = LED(4)
humanLedRed = LED(20)
humanLedGreen = LED(21)

try:                        # 프로그램이 종료될 때까지 무한 반복합니다.
    while 1:
        carLedRed.value = 0      # [상태 1] 차량 초록불, 보행자 빨간불 (3초 유지), # 차량 빨강 꺼짐.
        carLedYellow.value = 0   # 차량 노랑 꺼짐.
        carLedGreen.value = 1    # 차량 초록 켜짐.
        humanLedRed.value = 1    # 보행자 빨강 켜짐.
        humanLedGreen.value = 0  # 보행자 초록 켜짐.
        sleep(3.0)               # 3초 대기.
        carLedRed.value = 0      # [상태 2] 차량 노란불, 보행자 빨간불 (1초 유지), # 차량 빨강 꺼짐.
        carLedYellow.value = 1   # 차량 노랑 켜짐.
        carLedGreen.value = 0    # 차량 초록 꺼짐.
        humanLedRed.value = 1    # 보행자 빨강 유지.
        humanLedGreen.value = 0  # 보행자 초록 꺼짐.
        sleep(1.0)               # 1초 대기.
        carLedRed.value = 1      # [상태 3] 차량 빨간불, 보행자 초록불 (3초 유지), # 차량 빨강 켜짐.
        carLedYellow.value = 0   # 차량 노랑 꺼짐.
        carLedGreen.value = 0    # 차량 초록 꺼짐.
        humanLedRed.value = 0    # 보행자 빨강 꺼짐.
        humanLedGreen.value = 1  # 보행자 초록 켜짐.
        sleep(3.0)               # 3초 대기.
    
except KeyboardInterrupt:        # 사용자가 Ctrl + C를 눌러 프로그램을 중단할 때 발생하는 예외를 처리합니다
    pass

carLedRed.value = 0              # 프로그램 종료 시 모든 LED를 꺼서 안전하게 마무리합니다.
carLedYellow.value = 0
carLedGreen.value = 0
humanLedRed.value = 0
humanLedGreen.value = 0