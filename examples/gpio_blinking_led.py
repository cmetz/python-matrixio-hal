from matrixio_hal import GPIO
import time

# new pin 0
pin0 = GPIO.Pin(0)

# set pin to output mode
pin0.mode = GPIO.MODE_OUT

while True:
    # toggeling high(1) and low(0)
    pin0.value ^= GPIO.VALUE_HIGH
    time.sleep(0.5)

