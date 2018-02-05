from matrixio_hal import everloop
from collections import deque
import time

images = []
# generating 3 images with the lengths of 11
for img in range(3):
    image = everloop.Image(start = 11 * img, size = 11)
    image.leds[0].red = 5
    cnt = 1
    for i in range(1, len(image.leds)):
        if i <= 5:
            image.leds[i].red = 5
            image.leds[i].blue = cnt // 2
            cnt += 1
        else:
            image.leds[i].red = 5
            image.leds[i].green = cnt // 2
            cnt -= 1
    images.append(image)

#add additional image with only 2 leds, to fill up the 35 led array
image = everloop.Image(start = 33, size = 2)
image.leds[0].blue = 3
image.leds[1].red = 3
images.append(image)

while True:
    for image in images:
        image.render()

    images[0].rotate(1)
    images[1].rotate(-1)
    images[2].rotate(1)
    #images[3].rotate(1)
    time.sleep(0.1)
