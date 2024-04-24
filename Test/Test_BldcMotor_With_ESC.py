import RPi.GPIO as GPIO
import time

# 모터를 연결한 GPIO 핀 번호
ESC_PIN = 12  # 예시로 GPIO 핀 번호를 12번으로 설정

# PWM 주파수 설정
PWM_FREQ = 50  # Hz

# PWM 신호의 duty cycle 범위 (단위: %)
DUTY_MIN = 5
DUTY_MAX = 10

def setup():
    GPIO.setmode(GPIO.BOARD)  # BOARD 모드로 설정
    GPIO.setup(ESC_PIN, GPIO.OUT)
    pwm = GPIO.PWM(ESC_PIN, PWM_FREQ)
    pwm.start(0)
    return pwm

def set_speed(pwm, speed):
    duty = (speed / 100.0) * (DUTY_MAX - DUTY_MIN) + DUTY_MIN
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # 모터 속도가 변화할 시간을 주기 위한 대기 시간

def loop(pwm):
    try:
        while True:
            speed = float(input("Enter motor speed (0-100): "))
            if 0 <= speed <= 100:
                set_speed(pwm, speed)
            else:
                print("Speed out of range (0-100)")
    except KeyboardInterrupt:
        print("Exiting program")
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    pwm = setup()
    loop(pwm)
