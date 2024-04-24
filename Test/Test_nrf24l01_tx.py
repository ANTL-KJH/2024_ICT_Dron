import RPi.GPIO as GPIO
import spidev
import time

# SPI 인터페이스 초기화
spi = spidev.SpiDev()
spi.open(0, 0)  # (버스, 디바이스)

# NRF24L01 모듈과의 통신을 위한 설정
spi.max_speed_hz = 1000000
spi.mode = 0

# NRF24L01 모듈의 CE와 CSN 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)  # CE 핀
GPIO.setup(8, GPIO.OUT)   # CSN 핀

# CE 핀을 LOW로 설정하여 모듈을 대기 모드로 전환
GPIO.output(25, GPIO.LOW)

# 파이프 주소 설정
pipe_address = [0xE7, 0xE7, 0xE7, 0xE7, 0xE7]

# 송신 모드로 전환
def tx_mode():
    GPIO.output(25, GPIO.LOW)
    spi.xfer([0b11101000])  # TX 모드로 전환
    GPIO.output(25, GPIO.HIGH)

# 데이터 송신
def send_data(data):
    GPIO.output(8, GPIO.LOW)  # CSN 핀 LOW로 설정하여 SPI 통신 시작
    spi.xfer([0b10100000])    # 데이터 송신 명령과 데이터 파이프 주소 전송
    for byte in pipe_address:
        spi.xfer([byte])
    spi.xfer(data)            # 데이터 전송
    GPIO.output(8, GPIO.HIGH) # CSN 핀 HIGH로 설정하여 SPI 통신 종료

try:
    while True:
        # 송신 모드로 전환
        tx_mode()

        # 보낼 데이터
        data_to_send = [0xAA, 0xBB, 0xCC, 0xDD]  # 예시 데이터

        # 데이터 송신
        send_data(data_to_send)
        print("Sent:", data_to_send)

        time.sleep(1)  # 1초 대기 후 반복

except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
