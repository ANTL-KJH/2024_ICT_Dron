import RPi.GPIO as GPIO
import time
import os

# GPIO 핀 번호 설정
switch1_pin = 11  # 보드 기준 핀 번호
switch2_pin = 15  # 보드 기준 핀 번호
switch3_pin = 36
switch4_pin = 37
# GPIO 모드 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀 업 설정
GPIO.setup(switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀 업 설정
GPIO.setup(switch3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # 현재 스위치 상태 읽기
        switch1_state = GPIO.input(switch1_pin)
        switch2_state = GPIO.input(switch2_pin)
        switch3_state = GPIO.input(switch3_pin)
        switch4_state = GPIO.input(switch4_pin)

        os.system('clear')
        # 스위치 상태 출력
        print("스위치 1 상태:", "ON" if switch1_state == GPIO.LOW else "OFF")
        print("스위치 2 상태:", "ON" if switch2_state == GPIO.LOW else "OFF")
        print("스위치 3 상태:", "ON" if switch3_state == GPIO.LOW else "OFF")
        print("스위치 4 상태:", "ON" if switch4_state == GPIO.LOW else "OFF")


        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()  # GPIO 설정 초기화
