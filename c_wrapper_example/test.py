import matrixio_hal_wrap
import time
import random

bus = matrixio_hal_wrap.WishboneBus()

bus.SpiInit()

ev = matrixio_hal_wrap.Everloop()
ev.Setup(bus)
img = matrixio_hal_wrap.EverloopImage()

while True:
    for i in range(0, len(img.leds)):
        img.leds[i].red = random.randint(0, 10)
        img.leds[i].blue = random.randint(0, 10)
        img.leds[i].green = random.randint(0, 10)

    ev.Write(img)
    time.sleep(0.1)
