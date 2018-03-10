from . import bus
from . import matrixio_cpp_hal
from functools import wraps
import atexit

_gpio_control = matrixio_cpp_hal.PyGPIOControl()
_gpio_control.Setup(bus.bus)

MODE_IN = 0
MODE_OUT = 1

VALUE_LOW = 0
VALUE_HIGH = 1

FUNCTION_NORMAL = 0
FUNCTION_PWM = 1

atexit_cleanup_gpio = True
_gpio_used = False

def _is_using_gpio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _gpio_used
        _gpio_used = True
        return f(*args, **kwargs)
    return wrapper

class Pin(object):
    def __init__(self, pin):
        if pin < 0 or pin > 16:
            raise ValueError("wrong pin {}".format(pin))
        self.pin = pin
        self._mode = 0
        self._function = 0
        self.mode = 0
        self.function = 0
        self.value = 0
        
    @property
    def mode(self):
        return self._mode

    @mode.setter
    @_is_using_gpio
    def mode(self, mode):
        if mode not in [0, 1]:
            raise ValueError("Mode {} is not 0 or 1".format(mode))
        self._mode = mode
        return _gpio_control.SetMode(self.pin, self._mode)

    @property
    def value(self):
        return _gpio_control.GetGPIOValue(self.pin)

    @value.setter
    @_is_using_gpio
    def value(self, value):
        if value not in [0, 1]:
            raise ValueError("Value {} is not 0 or 1".format(mode))
        return _gpio_control.SetGPIOValue(self.pin, value)

    @property
    def function(self):
        return self._function

    @function.setter
    @_is_using_gpio
    def function(self, function):
        self._function = function
        return _gpio_control.SetFunction(self.pin, function)

class PWMBank(object):
    def __init__(self, frequency=100, bank=0):
        if bank != 0:
            raise ValueError("Only bank 0 is supported, due to matrix bug")
        self._bank = bank
        self._frequency = 0
        self._prescaler = 0
        self._period_counter = 0
        self.frequency = frequency

    @property
    def frequency(self):
        return self._frequency
    
    @frequency.setter
    @_is_using_gpio
    def frequency(self, frequency):
        period = 1.0 / frequency
        prescaler = 0
        while int(period * bus.FPGA_FREQUENCY / ((1 << (prescaler)) * 2)) > 65535:
            prescaler += 1
        period_counter = int((period * bus.FPGA_FREQUENCY) / ((1 << prescaler)*2))
        self._prescaler = prescaler
        self._period_counter = period_counter
        _gpio_control.SetPrescaler(self._bank, self._prescaler)
        _gpio_control.SetPeriod(self._bank, self._period_counter)


class PWM(object):
    def __init__(self, channel, bank):
        self._bank = bank
        self._pin = Pin(channel)
        self._duty = 0
        self._started = False

    @property
    def duty(self):
        return self._duty

    @duty.setter
    def duty(self, duty):
        if duty < 0 or duty > 100:
            raise ValueError("Duty not in range of 0 - 100%")
        self._duty = duty
        if self._started:
            self._enable_duty()

    def start(self, duty = None):
        if duty is not None:
            self.duty = duty
        self._enable_duty()

    @_is_using_gpio
    def _enable_duty(self):
        if not self._started:
            self._started = True
            self._pin.mode = MODE_OUT
            self._pin.value = VALUE_LOW
            self._pin.function = FUNCTION_PWM
        duty_counter = int(self._bank._period_counter / 100.0 * self._duty)
        _gpio_control.SetDuty(self._bank._bank, self._pin.pin, duty_counter)

    @_is_using_gpio
    def stop(self):
        if self._started:
            _gpio_control.SetDuty(self._bank._bank, self._pin.pin, 0)
            self._pin.mode = MODE_IN
            self._pin.value = VALUE_LOW
            self._pin.function = FUNCTION_NORMAL
        self._stated = False
        

@atexit.register
def cleanup():
    if atexit_cleanup_gpio and _gpio_used:
        for i in range(0, 17):
            _gpio_control.SetFunction(i, 0)
            _gpio_control.SetGPIOValue(i, 0)
            _gpio_control.SetMode(i, 0)
