import bus

CREATOR_SIZE = 35

COLORS = {
        "red":    [10,  0,  0],
        "green":  [ 0, 10,  0],
        "blue":   [ 0,  0, 10],
        "yellow": [10,  5,  0],
        "purple": [10,  0,  5],
        "cyan":   [ 0, 10,  5],
        "orange": [10,  2,  0]
        }
COLOR_NAMES = list(COLORS)

class Color:
    def __init__(self, red=0, green=0, blue=0, white=0, color=None):
        if color:
            self.set_color(color)
        else:
            self.red = red
            self.green = green
            self.blue = blue
        self.white = white

    def set_color(self, color):
        self.red, self.green, self.blue = COLORS[color]

class Image:
    def __init__(self, start=0, size=CREATOR_SIZE):
        self.start = start
        self.size = size
        self.leds = [Color() for _ in range(size)]
        self.rotate_offset = 0

    def rotate(self, direction=1):
        self.rotate_offset = (self.rotate_offset + direction)  % self.size

    def render(self):
        data = []
        for i in range(len(self.leds)):
            index = (i + self.size - self.rotate_offset) % self.size
            data.extend([
                self.leds[index].green, 
                self.leds[index].red,
                self.leds[index].blue,
                self.leds[index].white])
        bus.write(bus.EVERLOOP_ADR + self.start * 2, data)

def set_led(index, color, size=CREATOR_SIZE):
    index = index % size
    bus.write(bus.EVERLOOP_ADR + index * 2, [color.green, color.red, color.blue, color.white])

