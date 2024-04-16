import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
switch1_pin = 11  # 보드 기준 핀 번호
switch2_pin = 12  # 보드 기준 핀 번호

# GPIO 모드 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 풀 업 설정
GPIO.setup(switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 풀 업 설정

# 스위치 1의 이전 상태를 저장하기 위한 변수
switch1_prev_state = GPIO.input(switch2_pin)

# 스위치 2의 이전 상태를 저장하기 위한 변수
switch2_prev_state = GPIO.input(switch2_pin)

# 스위치 1의 인터럽트 처리 함수
def switch1_callback(channel):
    global switch1_prev_state
    current_state = GPIO.input(switch1_pin)
    if current_state != switch1_prev_state:
        switch1_prev_state = current_state
        if current_state == GPIO.LOW:
            print("스위치 1이 눌렸습니다.")
        else:
            print("스위치 1이 떨어졌습니다.")
        switch1_prev_state = current_state

# 스위치 2의 인터럽트 처리 함수
def switch2_callback(channel):
    global switch2_prev_state
    current_state = GPIO.input(switch2_pin)
    if current_state != switch2_prev_state:
        switch2_prev_state = current_state
        if current_state == GPIO.LOW:
            print("스위치 2가 눌렸습니다.")
        else:
            print("스위치 2가 떨어졌습니다.")
        switch2_prev_state = current_state

# 인터럽트 이벤트 설정
GPIO.add_event_detect(switch1_pin, GPIO.BOTH, callback=switch1_callback, bouncetime=200)
GPIO.add_event_detect(switch2_pin, GPIO.BOTH, callback=switch2_callback, bouncetime=200)

try:
    while True:
        # 메인 루프가 계속 실행되도록 유지
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()  # GPIO 설정 초기화
