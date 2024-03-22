import smbus
import time

# Define I2C address of MPU9250
MPU9250_ADDRESS = 0x68

# Define registers of MPU9250
MPU9250_ACCEL_XOUT_H = 0x3B
MPU9250_PWR_MGMT_1 = 0x6B

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

try:
    while True:
        accel_x, accel_y, accel_z = read_accel_data()
        print("Acceleration: X={}, Y={}, Z={}".format(accel_x, accel_y, accel_z))
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
