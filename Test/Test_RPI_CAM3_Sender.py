import cv2
from picamera2 import Picamera2
import socket

class VideoStreamer:
    def __init__(self, video_model):
        self.__video_model = video_model
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 소켓 설정 등 추가적인 초기화 작업

    def start_streaming(self):
        picam2 = Picamera2()
        picam2.preview_configuration.main.size = (640, 480)
        picam2.preview_configuration.main.format = "BGR888"
        picam2.preview_configuration.align()
        picam2.configure("preview")
        picam2.start()

        while True:
            s = self.__video_model.get_frame()  # 46080 bytes
            packet_size = 46080  # 각 패킷의 크기

            for i in range(20):
                start_idx = i * packet_size
                end_idx = (i + 1) * packet_size
                packet_data = bytes([i]) + s[start_idx:end_idx]

                self.video_socket.sendto(packet_data, ("165.229.125.128", 9999))

            # 키 입력을 기다리고 'q'가 입력되면 루프를 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # OpenCV 창 닫기 및 Picamera2 종료
        cv2.destroyAllWindows()
        picam2.stop()

class VideoModel:
    def get_frame(self):
        # Picamera2로부터 프레임을 캡처하고 반환하는 로직을 여기에 구현
        return frame_data

def main():
    video_model = VideoModel()
    video_streamer = VideoStreamer(video_model)
    video_streamer.start_streaming()

if __name__ == "__main__":
    main()
