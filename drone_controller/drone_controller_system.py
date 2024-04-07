import drone_controller_switch
import drone_controller_joystick
import drone_controller_information
from threading import Thread

class class_Drone_Controller_System:
    def __init__(self):
        self.info = drone_controller_information.class_Drone_Controller_Information()
        self.controllerJoystick_L = drone_controller_joystick.class_Drone_Controller_Joystick(0, 0, 1, 2, 0, 1, self)
        self.controllerJoystick_R = drone_controller_joystick.class_Drone_Controller_Joystick(1, 0, 1, 2, 0, 2, self)

    def start_Drone_Controller(self):
        print("SYSTEM ALARM::Drone Controller Started")
        thread_Joystick_Left = Thread(target=self.controllerJoystick_L.run_joystick)
        thread_Joystick_Right = Thread(target=self.controllerJoystick_R.run_joystick)
        thread_Joystick_Left.start()
        thread_Joystick_Right.start()


    def run_drone_controller(self):
        # controllerSwitch = drone_controller_switch.class_Drone_Controller_Switch(self)

        while True:
            print("Joystick Left(x:{}, y:{}, val:{}".format(self.info.joystick_Left_x, self.info.joystick_Left_y,
                                                            self.info.joystick_Left_val))
            print("Joystick Right(x:{}, y:{}, val:{}".format(self.info.joystick_Right_x, self.info.joystick_Right_y,
                                                             self.info.joystick_Right_val))
