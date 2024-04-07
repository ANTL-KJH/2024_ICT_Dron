import cv2
import numpy as np
import socket

class class_Drone_Controller_VideoStreamer:
    def __init__(self):
        self.ip_address = '192.168.32.1'    # 드론 ip
        self.port = 12345
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_address, self.port))

    def receive_video(self):
        while True:
            try:
                data, _ = self.socket.recvfrom(65535)
                # 데이터를 디코딩하여 이미지로 변환
                frame = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(frame, flags=1)
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print(f"Error receiving video: {e}")
                break

    def run_VideoStreamer(self):
        self.receive_video()