import spidev
import time
import drone_controller.drone_controller_information

class class_Drone_Controller_Joystick:
    def __init__(self, bus, device, x_channel, y_channel, switch_channel, classifyNum, ctrl_info):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.x_channel = x_channel
        self.y_channel = y_channel
        self.switch_channel = switch_channel
        self.ctrl_info = ctrl_info
        self.classifyNum = classifyNum

    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def read_position(self):
        x_pos = self.read_channel(self.x_channel)
        y_pos = self.read_channel(self.y_channel)
        switch_val = self.read_channel(self.switch_channel)
        if self.classifyNum == 1:
            self.ctrl_info.joystick_Left_x = x_pos
            self.ctrl_info.joystick_Left_y = y_pos
            self.ctrl_info.joystick_Left_val = switch_val
        elif self.classifyNum == 2:
            self.ctrl_info.joystick_Right_x = x_pos
            self.ctrl_info.joystick_Right_y = y_pos
            self.ctrl_info.joystick_Right_val = switch_val
        #return x_pos, y_pos, switch_val

    def run_joystick(self):
        while True:
            self.read_position()
