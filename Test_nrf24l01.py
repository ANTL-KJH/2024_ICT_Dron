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

# 수신 모드로 전환
def rx_mode():
    GPIO.output(25, GPIO.LOW)
    spi.xfer([0b11101010])  # RX 모드로 전환
    GPIO.output(25, GPIO.HIGH)

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

# 데이터 수신
def receive_data():
    rx_mode()
    time.sleep(0.1)  # NRF24L01 모듈이 수신할 수 있도록 충분한 시간 대기
    GPIO.output(8, GPIO.LOW)  # CSN 핀 LOW로 설정하여 SPI 통신 시작
    received_data = spi.xfer([0b01100001] + [0xFF] * 32)  # 데이터 수신 명령과 최대 길이의 데이터를 전송하여 데이터 수신
    GPIO.output(8, GPIO.HIGH) # CSN 핀 HIGH로 설정하여 SPI 통신 종료
    return received_data[1:]  # 첫 번째 바이트는 상태 바이트이므로 제외하고 반환

try:
    while True:
        # 데이터 수신
        received_data = receive_data()
        print("Received:", received_data)

        # 수신된 데이터에 대한 응답 보내기
        response_data = [0xAA, 0xBB, 0xCC, 0xDD]  # 임의의 응답 데이터
        send_data(response_data)
        print("Sent:", response_data)

        time.sleep(1)  # 1초 대기 후 반복

except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()