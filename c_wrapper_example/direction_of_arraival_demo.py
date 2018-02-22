# Copyright 2016 <Admobilize>
# All rights reserved.
# example in python ported from:
# https://github.com/matrix-io/matrix-creator-hal/blob/master/demos/direction_of_arrival_demo.cpp
 
import matrixio_hal_wrap
import math
import time

SAMPLING_RATE = 16000


LED_OFFSET = [23, 27, 32, 1, 6, 10, 14, 19]
LUT = [1, 2, 10, 200, 10, 2, 1]


if __name__ == '__main__':

    bus = matrixio_hal_wrap.WishboneBus()
    bus.SpiInit()

    mics = matrixio_hal_wrap.MicrophoneArray()
    mics.Setup(bus)

    everloop = matrixio_hal_wrap.Everloop() 
    everloop.Setup(bus)

    image1d = matrixio_hal_wrap.EverloopImage()

    mics.SetSamplingRate(SAMPLING_RATE)
    mics.ShowConfiguration()

    doa = matrixio_hal_wrap.DirectionOfArrival(mics)
    doa.Init()

    while True:
        mics.Read()

        doa.Calculate()

        azimutal_angle = doa.GetAzimutalAngle() * 180 / math.pi
        polar_angle = doa.GetPolarAngle() * 180 / math.pi
        mic = doa.GetNearestMicrophone()

        print("azimutal angle = {}, polar angel = {}, mic = {}".format(azimutal_angle, polar_angle, mic))

        for i in range(0, len(image1d.leds)):
            image1d.leds[i].blue = 0

        j = 0
        for j, i in enumerate(range(LED_OFFSET[mic] - 3, LED_OFFSET[mic] + 4)):
            if i < 0:
                image1d.leds[len(image1d.leds) + i].blue = LUT[j]
            else:
                image1d.leds[i % len(image1d.leds)].blue = LUT[j]

        everloop.Write(image1d)

