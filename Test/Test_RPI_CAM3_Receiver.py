import cv2
import socket
import numpy as np

UDP_IP = "0.0.0.0"
UDP_PORT = 9999

# 패킷을 저장할 버퍼
frame_buffer = [None] * 20

# 소켓 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    # 패킷 수신
    data, addr = sock.recvfrom(46081)  # 하나의 패킷 크기는 46081 바이트 (1 바이트는 패킷의 인덱스)

    # 패킷에서 인덱스와 데이터 추출
    index = data[0]
    packet_data = data[1:]

    # 프레임 버퍼에 패킷 데이터 삽입
    frame_buffer[index] = packet_data

    # 모든 패킷을 수신했는지 확인
    if all(frame_buffer):
        # 모든 패킷을 모아서 하나의 프레임으로 복원
        frame_data = b''.join(frame_buffer)

        # 프레임 데이터를 NumPy 배열로 변환
        frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((480, 640, 3))

        # OpenCV를 사용하여 프레임 표시
        cv2.imshow('Received Frame', frame)

        # 키 입력을 기다리고 'q'가 입력되면 루프를 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# OpenCV 창 닫기
cv2.destroyAllWindows()
