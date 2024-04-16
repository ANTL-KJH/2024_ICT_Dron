import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
switch1_pin = 11  # 보드 기준 핀 번호
switch2_pin = 12  # 보드 기준 핀 번호

# GPIO 모드 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 풀 업 설정
GPIO.setup(switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 풀 업 설정

try:
    while True:
        # 스위치 1 상태 확인
        if GPIO.input(switch1_pin) == GPIO.LOW:
            print("스위치 1이 눌렸습니다.")
            # 여기에 스위치 1이 눌렸을 때 실행할 작업을 추가하세요.
            time.sleep(0.2)  # 디바운스를 위한 딜레이

        # 스위치 2 상태 확인
        if GPIO.input(switch2_pin) == GPIO.LOW:
            print("스위치 2가 눌렸습니다.")
            # 여기에 스위치 2가 눌렸을 때 실행할 작업을 추가하세요.
            time.sleep(0.2)  # 디바운스를 위한 딜레이

except KeyboardInterrupt:
    GPIO.cleanup()  # GPIO 설정 초기화
