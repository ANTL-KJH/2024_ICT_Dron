import pyrealsense2 as rs
import math


def main():
    # Realsense pipeline을 초기화합니다.
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.accel)
    config.enable_stream(rs.stream.gyro)

    # Realsense pipeline을 시작합니다.
    profile = pipeline.start(config)

    try:
        while True:
            # 프레임을 가져옵니다.
            frames = pipeline.wait_for_frames()
            for frame in frames:
                # IMU 데이터를 가져옵니다.
                if frame.is_motion_frame():
                    motion_data = frame.as_motion_frame().get_motion_data()
                    if frame.get_profile().stream_type() == rs.stream.accel:
                        accel_data = (motion_data.x, motion_data.y, motion_data.z)
                    elif frame.get_profile().stream_type() == rs.stream.gyro:
                        gyro_data = (motion_data.x, motion_data.y, motion_data.z)

            # 가속도 및 자이로 스코프 데이터를 사용하여 yaw, pitch, roll 값을 계산합니다.
            accel_roll = math.atan2(accel_data[1], accel_data[2])
            accel_pitch = math.atan2(-accel_data[0], math.sqrt(accel_data[1] ** 2 + accel_data[2] ** 2))

            gyro_roll = gyro_data[0]
            gyro_pitch = gyro_data[1]
            gyro_yaw = gyro_data[2]

            # Yaw, Pitch, Roll 값을 출력합니다.
            print("Yaw:", gyro_yaw, "Pitch:", accel_pitch, "Roll:", accel_roll)

    finally:
        # Realsense pipeline을 정리합니다.
        pipeline.stop()


if __name__ == "__main__":
    main()
