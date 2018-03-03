from matrixio_hal import sensors, everloop
import math
import time

CALIBRATION_SAMPLES = 600


def get_heading(imu, mag_bias=[0.0, 0.0, 0.0]):
    imu.update()


    mx = -(imu.mag_x - mag_bias[0])
    my = imu.mag_y - mag_bias[1]
    mz = imu.mag_z - mag_bias[2]

    # tilt correction
    norm = 1.0 / math.sqrt(imu.accel_x ** 2 + imu.accel_y ** 2 + imu.accel_z ** 2)
    accel_x_norm = imu.accel_x * norm
    accel_y_norm = imu.accel_y * norm
    pitch = math.asin(accel_x_norm)
    roll = -1 * math.asin(accel_y_norm / math.cos(pitch))
    mx = mx * math.cos(pitch) + my * math.sin(roll)*math.sin(pitch) + mz * math.cos(roll) * math.sin(pitch)
    my = my * math.cos(roll) - mz * math.sin(roll)

    # calculate heading
    heading = math.atan2(my, mx) * 180 / math.pi
    if heading < 0:
        heading += 360
    return heading


def calibrate_compass(imu):
    # calibrate
    mag_bias = [0.0, 0.0, 0.0]
    mag_min = [0.0, 0.0, 0.0]
    mag_max = [0.0, 0.0, 0.0]

    print("Starting calibration:")
    print("Wave your creator in a 8 form for {} seconds.".format(CALIBRATION_SAMPLES // 100))
    for sample in range(CALIBRATION_SAMPLES):
        imu.update()
        mag_min = [min(v) for v in zip(mag_min, [imu.mag_x, imu.mag_y, imu.mag_z])]
        mag_max = [max(v) for v in zip(mag_max, [imu.mag_x, imu.mag_y, imu.mag_z])]

        # comment in to check if all min / max is covered
        #if sample % 100 == 0:
        #    print(mag_min, mag_max)
        time.sleep(0.01)

    mag_bias = [sum(v) / 2 for v in zip(mag_min, mag_max)]
    print("Calibration ended")

    return mag_bias


if __name__ == '__main__':
    imu = sensors.IMU()
    img = everloop.Image()

    mag_bias = calibrate_compass(imu)

    while True:
        heading = get_heading(imu, mag_bias)
        blue_led = int(heading * 35 / 360)
        red_led = (blue_led + 17) % 34;
        for i, l in enumerate(img.leds):
            l.blue = 50 if i == blue_led else 0
            l.red = 50 if i == red_led else 0
        img.render()
        print(heading)
        time.sleep(0.1)

