import drone_controller_switch
import drone_controller_joystick
import drone_controller_information
import drone_controller_videostreamer
from threading import Thread, Lock
import socket
import pickle

class class_Drone_Controller_System:
    def __init__(self):
        self.info = drone_controller_information.class_Drone_Controller_Information()
        self.controllerJoystick_L = drone_controller_joystick.class_Drone_Controller_Joystick(0, 0, 1, 2, 0, 1, self)
        self.controllerJoystick_R = drone_controller_joystick.class_Drone_Controller_Joystick(1, 0, 1, 2, 0, 2, self)
        self.videoStreamer = drone_controller_videostreamer.class_Drone_Controller_VideoStreamer()
        self.socket_lock = Lock()  # 소켓 동기화를 위한 Lock 객체
        self.target_ip = '192.168.32.10'  # 드론 IP 주소
        self.target_port = 12345  # port
        self.socket = None
    def start_Drone_Controller(self):
        print("SYSTEM ALARM::Drone Controller Started")
        thread_Joystick_Left = Thread(target=self.controllerJoystick_L.run_joystick)
        thread_Joystick_Right = Thread(target=self.controllerJoystick_R.run_joystick)
        thread_VideoStream = Thread(target=self.videoStreamer.run_VideoStreamer())
        thread_Joystick_Left.start()
        thread_Joystick_Right.start()

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
            
    def run_drone_controller(self):
        # controllerSwitch = drone_controller_switch.class_Drone_Controller_Switch(self)
        self.start_Drone_Controller()
        while True:
            print("Joystick Left(x:{}, y:{}, val:{}".format(self.info.joystick_Left_x, self.info.joystick_Left_y,
                                                            self.info.joystick_Left_val))
            print("Joystick Right(x:{}, y:{}, val:{}".format(self.info.joystick_Right_x, self.info.joystick_Right_y,
                                                             self.info.joystick_Right_val))

            joystick_data = [self.info.joystick_Left_x, self.info.joystick_Left_y, self.info.joystick_Left_val, self.info.joystick_Right_x, self.info.joystick_Right_y, self.info.joystick_Right_val]
            # 조이스틱 값 TCP 전송
            self.send_joystick_data(joystick_data)