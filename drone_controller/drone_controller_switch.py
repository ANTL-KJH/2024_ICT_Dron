import RPi.GPIO as GPIO
import time
import drone_controller.drone_controller_information

class class_Drone_Controller_Switch:
    def __init__(self, ctrl_info):
        self.switch1_pin = 11
        self.switch2_pin = 13
        self.switch3_pin = 36
        self.switch4_pin = 37
        self.ctrl_info = ctrl_info
        # GPIO 설정
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # 스위치 인터럽트 핸들러 등록
        GPIO.add_event_detect(self.switch1_pin, GPIO.FALLING, callback=self.switch1_callback, bouncetime=200)
        GPIO.add_event_detect(self.switch2_pin, GPIO.FALLING, callback=self.switch2_callback, bouncetime=200)
        GPIO.add_event_detect(self.switch3_pin, GPIO.FALLING, callback=self.switch3_callback, bouncetime=200)
        GPIO.add_event_detect(self.switch4_pin, GPIO.FALLING, callback=self.switch4_callback, bouncetime=200)

    def switch1_callback(self, channel):
        self.ctrl_info.switch1 = GPIO.input(self.switch1_pin)

    def switch2_callback(self, channel):
        self.ctrl_info.switch2 = GPIO.input(self.switch2_pin)

    def switch3_callback(self, channel):
        self.ctrl_info.switch3 = GPIO.input(self.switch3_pin)

    def switch4_callback(self, channel):
        self.ctrl_info.switch4 = GPIO.input(self.switch4_pin)

    def cleanup(self):
        GPIO.cleanup()



