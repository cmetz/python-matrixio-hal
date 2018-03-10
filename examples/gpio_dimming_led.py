from matrixio_hal import GPIO
import time

# create new PWMBank with a frequency of 100Hz
# the Matrix has 4 banks 0-3, but only Bank0 (default) works currently
# each Bank can have it's own frequency
bank = GPIO.PWMBank(frequency=100)

# create new PWM - binding channel(pin)=0 and the bank configured above
# each bank can be assigned to multiple channels (pins) with their
# own duty
pwm = GPIO.PWM(channel=0, bank=bank)

# starting with a duty 5%
pwm.start(duty=5)
while True:
    # increase the duty by 1% restart at 50%
    # pwm.duty = is property with setter function
    # so setting the duty will have an instant effect
    # do not use this as a temporary caluclation variable
    # but you can use it to get the current duty
    pwm.duty = pwm.duty + 1 if pwm.duty + 1 <= 50 else 5
    time.sleep(0.1)

# this pwm.stop() would propably never been caled, as you need to
# stop this demo by using ctrl-c, but the atexit handler will
# cleanup the GPIOs anyway
# setting GPIO.atexit_cleanup_gpio = False would prevent this
pwm.stop()
