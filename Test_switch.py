import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
switch1_pin = 11  # 보드 기준 핀 번호
switch2_pin = 12  # 보드 기준 핀 번호

# GPIO 모드 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 풀 업 설정
GPIO.setup(switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 풀 업 설정

# 스위치 1의 인터럽트 처리 함수
def switch1_callback(channel):
    print("스위치 1의 상태가 변경되었습니다.")
    # 여기에 스위치 1의 상태에 따른 작업을 추가하세요.

# 스위치 2의 인터럽트 처리 함수
def switch2_callback(channel):
    print("스위치 2의 상태가 변경되었습니다.")
    # 여기에 스위치 2의 상태에 따른 작업을 추가하세요.

# 인터럽트 이벤트 설정
GPIO.add_event_detect(switch1_pin, GPIO.BOTH, callback=switch1_callback, bouncetime=200)
GPIO.add_event_detect(switch2_pin, GPIO.BOTH, callback=switch2_callback, bouncetime=200)

try:
    while True:
        # 메인 루프가 계속 실행되도록 유지
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()  # GPIO 설정 초기화
