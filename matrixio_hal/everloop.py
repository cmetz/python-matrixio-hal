import bus

CREATOR_SIZE = 35

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

class Color:
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

class Image:
    def __init__(self, start=0, size=CREATOR_SIZE, init_color_name='black'):
        self.start = start
        self.size = size
        self.leds = [Color(color_name=init_color_name) for _ in range(size)]
        self.rotate_offset = 0

    def rotate(self, direction=1):
        self.rotate_offset = (self.rotate_offset + direction)  % self.size

    def render(self):
        data = []
        for i in range(self.size):
            index = (i + self.size - self.rotate_offset) % self.size
            data.extend([
                self.leds[index].green, 
                self.leds[index].red,
                self.leds[index].blue,
                self.leds[index].white])
        if self.start + self.size <= CREATOR_SIZE:
            # image below or even max_size
            bus.write(bus.EVERLOOP_ADR + self.start * 2, data)
        else:
            # split images stepping over max_size
            bus.write(bus.EVERLOOP_ADR + self.start * 2, data[:(CREATOR_SIZE - self.start) * 4])
            bus.write(bus.EVERLOOP_ADR, data[(CREATOR_SIZE - self.start) * 4:])

def set_led(index, color, size=CREATOR_SIZE):
    index = index % size
    bus.write(bus.EVERLOOP_ADR + index * 2, [color.green, color.red, color.blue, color.white])

