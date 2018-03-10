from matrixio_hal import sensors

pressure = sensors.Pressure()

print("Altitude: {}".format(pressure.altitude))
print("Pressure: {}".format(pressure.pressure))
print("Temperature: {}".format(pressure.temperature))

