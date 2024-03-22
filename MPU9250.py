import smbus
import math
import time

# Define I2C address of MPU9250
MPU9250_ADDRESS = 0x68

# Define registers of MPU9250
MPU9250_ACCEL_XOUT_H = 0x3B
MPU9250_PWR_MGMT_1 = 0x6B
MPU9250_GYRO_XOUT_H = 0x43

# Constants for conversion
RAD_TO_DEG = 180.0 / math.pi

# Create a bus object
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# Initialize MPU9250
bus.write_byte_data(MPU9250_ADDRESS, MPU9250_PWR_MGMT_1, 0x00)

# Function to read accelerometer data
def read_accel_data():
    data = bus.read_i2c_block_data(MPU9250_ADDRESS, MPU9250_ACCEL_XOUT_H, 6)
    accel_x = (data[0] << 8) | data[1]
    accel_y = (data[2] << 8) | data[3]
    accel_z = (data[4] << 8) | data[5]

    # Convert to signed values
    if accel_x > 32767:
        accel_x -= 65536
    if accel_y > 32767:
        accel_y -= 65536
    if accel_z > 32767:
        accel_z -= 65536

    return accel_x, accel_y, accel_z

# Function to read gyro data
def read_gyro_data():
    data = bus.read_i2c_block_data(MPU9250_ADDRESS, MPU9250_GYRO_XOUT_H, 6)
    gyro_x = (data[0] << 8) | data[1]
    gyro_y = (data[2] << 8) | data[3]
    gyro_z = (data[4] << 8) | data[5]

    # Convert to signed values
    if gyro_x > 32767:
        gyro_x -= 65536
    if gyro_y > 32767:
        gyro_y -= 65536
    if gyro_z > 32767:
        gyro_z -= 65536

    return gyro_x, gyro_y, gyro_z

# Function to calculate Yaw, Pitch, and Roll
def calculate_yaw_pitch_roll(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z):
    # Calculate Yaw, Pitch, Roll using accelerometer and gyroscope data
    roll = math.atan2(accel_y, accel_z) * RAD_TO_DEG
    pitch = math.atan(-accel_x / math.sqrt(accel_y ** 2 + accel_z ** 2)) * RAD_TO_DEG

    gyro_x_rate = gyro_x / 131.0
    gyro_y_rate = gyro_y / 131.0
    gyro_z_rate = gyro_z / 131.0

    roll -= gyro_x_rate * 0.01
    pitch += gyro_y_rate * 0.01

    return roll, pitch

try:
    while True:
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        roll, pitch = calculate_yaw_pitch_roll(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
        print("Roll: {:.2f}, Pitch: {:.2f}".format(roll, pitch))
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
