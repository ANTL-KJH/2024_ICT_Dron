import drone_controller_information
from threading import Thread, Lock
import socket
import pickle
class class_drone_controller_datasender:

    def __init__(self, info):
        self.info = info
        self.socket_lock = Lock()  # 소켓 동기화를 위한 Lock 객체
        self.target_ip = '192.168.32.10'  # 드론 IP 주소
        self.target_port = 12345  # port
        self.socket = None
    def send_joystick_data(self, data):
        try:
            # 소켓이 없는 경우 생성
            if self.socket is None:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.target_ip, self.target_port))
            # 데이터를 직렬화하고 전송
            serialized_data = pickle.dumps(data)
            with self.socket_lock:
                self.socket.sendall(serialized_data)
        except Exception as e:
            print(f"Error sending joystick data: {e}")

    def run_data_sender(self):
        while True:


            joystick_data = [self.info.joystick_Left_x, self.info.joystick_Left_y, self.info.joystick_Left_val, self.info.joystick_Right_x, self.info.joystick_Right_y, self.info.joystick_Right_val]
            # 조이스틱 값 TCP 전송
            self.send_joystick_data(joystick_data)
