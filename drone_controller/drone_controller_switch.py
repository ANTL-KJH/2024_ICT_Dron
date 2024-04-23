import RPi.GPIO as GPIO
import time
import drone_controller.drone_controller_information

class class_Drone_Controller_Switch:
    def __init__(self, ctrl_info):
        self.switch1_pin = 11  # 보드 기준 핀 번호
        self.switch2_pin = 13  # 보드 기준 핀 번호
        self.switch3_pin = 36
        self.switch4_pin = 37
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀 업 설정
        GPIO.setup(self.switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀 업 설정
        GPIO.setup(self.switch3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def runSwitch(self):
        while True:
            # 현재 스위치 상태 읽기
            switch1_state = GPIO.input(self.switch1_pin)
            switch2_state = GPIO.input(self.switch2_pin)
            switch3_state = GPIO.input(self.switch3_pin)
            switch4_state = GPIO.input(self.switch4_pin)

            time.sleep(0.05)



