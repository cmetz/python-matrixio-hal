from matrixio_hal import sensors

humidity = sensors.Humidity()

print("Humidity: {}".format(humidity.humidity))
print("Temperature: {}".format(humidity.temperature))

