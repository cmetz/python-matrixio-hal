from matrixio_hal import everloop
import random
import time

cnt = 0
color = everloop.Color(color='orange')
color_clear = everloop.Color()
offset = 0
turn_on = True
while True:
    if cnt >= 35:
        cnt = 0
        turn_on = not turn_on
        if turn_on:
            if random.randint(0, 1) == 0:
                # choose from COLOR_NAMES
                color.set_color(random.choice(everloop.COLOR_NAMES))
            else:
                # completely random
                color.red, color.green, color.blue = [random.randint(0, 4) for _ in range(3)]
            offset = random.randint(0, 34)
            print('R:{} G:{} B:{}'.format(color.red, color.green, color.blue))

    if turn_on:
        everloop.set_led(cnt + offset, color)
    else:
        everloop.set_led(34 - cnt + offset, color_clear)
    time.sleep(0.05 if turn_on else 0.01)
    cnt += 1
