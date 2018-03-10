from . import matrixio_cpp_hal
from . import bus
from functools import wraps
import atexit
import time

EVERLOOP_SIZE = 35 if bus.MATRIX_DEVICE == 'creator' else 18

COLORS = {             #  R    G    B    W
        "black":       [  0,   0,   0,   0],
        "red":         [ 10,   0,   0,   0],
        "green":       [  0,  10,   0,   0],
        "blue":        [  0,   0,  10,   0],
        "yellow":      [ 10,   5,   0,   0],
        "purple":      [ 10,   0,   5,   0],
        "cyan":        [  0,  10,   5,   0],
        "orange":      [ 10,   2,   0,   0],
        "_flashlight": [255, 255, 255, 255]
        }
COLOR_NAMES = [c for c in list(COLORS) if not c.startswith('_')]

atexit_clear_everloop = True

_everloop_used = False

_cpp_ev_image = matrixio_cpp_hal.PyEverloopImage()
_cpp_ev = matrixio_cpp_hal.PyEverloop()
_cpp_ev.Setup(bus.bus)

def _is_using_everloop(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _everloop_used
        _everloop_used = True
        return f(*args, **kwargs)
    return wrapper

class Color(object):
    def __init__(self, red=0, green=0, blue=0, white=0, color_name=None):
        if color_name:
            self.set_by_name(color_name)
        else:
            self.red = red
            self.green = green
            self.blue = blue
            self.white = white

    def set_by_name(self, color_name):
        self.red, self.green, self.blue, self.white = COLORS[color_name]

class Image(object):
    def __init__(self, start=0, size=EVERLOOP_SIZE, init_color_name='black'):
        self.start = start
        self.size = size
        self.leds = [Color(color_name=init_color_name) for _ in range(size)]
        self.rotate_offset = 0

    def rotate(self, direction=1):
        self.rotate_offset = (self.rotate_offset + direction)  % self.size

    @_is_using_everloop
    def render(self):
        global _cpp_ev
        global _cpp_ev_image
        data = []
        for i in range(self.size):
            index = (i - self.rotate_offset) % self.size
            ev_index = (self.start + i) % EVERLOOP_SIZE
            _cpp_ev_image.leds[ev_index].red = self.leds[index].green
            _cpp_ev_image.leds[ev_index].green = self.leds[index].red
            _cpp_ev_image.leds[ev_index].blue = self.leds[index].blue
            _cpp_ev_image.leds[ev_index].white = self.leds[index].white
        _cpp_ev.Write(_cpp_ev_image)

@_is_using_everloop
def set_led(index, color):
    global _cpp_ev
    global _cpp_ev_image
    index = index % EVERLOOP_SIZE
    _cpp_ev_image.leds[index].red = color.green
    _cpp_ev_image.leds[index].green = color.red
    _cpp_ev_image.leds[index].blue = color.blue
    _cpp_ev_image.leds[index].white = color.white
    _cpp_ev.Write(_cpp_ev_image)

@atexit.register
def cleanup():
    if atexit_clear_everloop and _everloop_used:
        Image().render()

