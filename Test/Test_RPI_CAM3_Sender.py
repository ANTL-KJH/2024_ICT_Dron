import cv2
import socket
import pickle
import struct
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"  # BGR 형식으로 변경
picam2.preview_configuration.main.format = "RGB888"  # BGR 형식으로 변경
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# 수신 라즈베리파이의 IP 주소와 포트 번호 설정
receiver_ip = "192.168.50.126"
port = 8005

# 소켓 초기화
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    im = picam2.capture_array()
    cv2.imshow("Camera", im)
    # 영상을 직렬화하여 전송
    data = pickle.dumps(im)
    size = len(data)
    max_packet_size = 65000  # UDP 패킷 최대 크기
    num_packets = (size + max_packet_size - 1) // max_packet_size  # 올림 계산

    # 패킷을 여러 번에 걸쳐 전송
    for i in range(num_packets):
        start = i * max_packet_size
        end = min((i + 1) * max_packet_size, size)
        client_socket.sendto(data[start:end], (receiver_ip, port))

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 정리
cap.release()
cv2.destroyAllWindows()
client_socket.close()