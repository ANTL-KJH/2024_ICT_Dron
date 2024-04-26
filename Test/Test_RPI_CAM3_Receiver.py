import cv2
import socket
import numpy as np

# 수신 설정
IP_RECEIVER = "0.0.0.0"  # 모든 인터페이스에서 수신
PORT_RECEIVER = 8080  # 송신 코드와 동일한 포트 번호 사용
BUFFER_SIZE = 46081  # 송신 코드에서 사용한 조각 크기와 동일

# 소켓 초기화
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((IP_RECEIVER, PORT_RECEIVER))

try:
    received_data = b""
    num_slices = 20  # 송신 코드에서 전송한 조각 수

    while True:
        # 데이터 수신
        data, addr = receiver_socket.recvfrom(BUFFER_SIZE)
        slice_index = data[0]  # 전송된 데이터의 인덱스
        slice_data = data[1:]  # 전송된 데이터의 내용

        # 수신된 데이터를 저장
        received_data += slice_data

        # 모든 조각을 수신했을 때 화면에 영상 표시
        if len(received_data) >= num_slices * BUFFER_SIZE:
            # 모든 조각을 조립하여 이미지로 변환
            im = np.frombuffer(received_data, dtype=np.uint8)
            im = im.reshape((480, 640, 3))

            # 영상 표시
            cv2.imshow("Received Video", im)

            # 수신된 데이터 초기화
            received_data = b""

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # OpenCV 창 닫기 및 소켓 닫기
    cv2.destroyAllWindows()
    receiver_socket.close()
