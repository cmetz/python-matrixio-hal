from matrixio_hal import sensors
import time

# IMU
imu = sensors.IMU()
while True:
    print("\x1B[2J")
    print("yaw: {}".format(imu.yaw))
    print("pitch: {}".format(imu.pitch))
    print("roll: {}".format(imu.roll))
    print("accel_x: {}".format(imu.accel_x))
    print("accel_y: {}".format(imu.accel_y))
    print("accel_z: {}".format(imu.accel_z))
    print("gyro_x: {}".format(imu.gyro_x))
    print("gyro_y: {}".format(imu.gyro_y))
    print("gyro_z: {}".format(imu.gyro_z))
    print("mag_x: {}".format(imu.mag_x))
    print("mag_y: {}".format(imu.mag_y))
    print("mag_z: {}".format(imu.mag_z))
    time.sleep(0.1)
    imu.update()
