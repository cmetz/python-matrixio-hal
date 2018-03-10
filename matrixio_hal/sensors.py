from . import matrixio_cpp_hal
from . import bus
import abc

class BaseSensor(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, sensor_cls, data_cls):
        self._data = data_cls()
        self._sensor = sensor_cls()
        self._sensor.Setup(bus.bus)
    
    def _update_sensor(self): 
        self._sensor.Read(self._data)

    @abc.abstractmethod
    def update(self):
        pass

class IMU(BaseSensor):
    def __init__(self):
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0
        self.gyro_x = 0.0
        self.gyro_y = 0.0
        self.gyro_z = 0.0
        self.mag_x = 0.0
        self.mag_y = 0.0
        self.mag_z = 0.0
        super(IMU, self).__init__(matrixio_cpp_hal.PyIMUSensor, matrixio_cpp_hal.PyIMUData)
        self.update()

    def update(self):
        super(IMU, self)._update_sensor()
        self.yaw = self._data.yaw
        self.pitch = self._data.pitch
        self.roll = self._data.roll
        self.accel_x = self._data.accel_x
        self.accel_y = self._data.accel_y
        self.accel_z = self._data.accel_z
        self.gyro_x = self._data.gyro_x
        self.gyro_y = self._data.gyro_y
        self.gyro_z = self._data.gyro_z
        self.mag_x = self._data.mag_x
        self.mag_y = self._data.mag_y
        self.mag_z = self._data.mag_z

class Pressure(BaseSensor):
    def __init__(self):
        self.altitude = 0.0
        self.pressure = 0.0
        self.temperature = 0.0
        super(Pressure, self).__init__(matrixio_cpp_hal.PyPressureSensor, matrixio_cpp_hal.PyPressureData)
        self.update()

    def update(self):
        super(Pressure, self)._update_sensor()
        self.altitude = self._data.altitude
        self.pressure = self._data.pressure
        self.temperature = self._data.temperature


class UV(BaseSensor):
    def __init__(self):
        self.uv = 0.0
        super(UV, self).__init__(matrixio_cpp_hal.PyUVSensor, matrixio_cpp_hal.PyUVData)
        self.update()

    def update(self):
        super(UV, self)._update_sensor()
        self.uv = self._data.uv

class Humidity(BaseSensor):
    def __init__(self):
        self.humidity = 0.0
        self.temperature = 0.0
        super(Humidity, self).__init__(matrixio_cpp_hal.PyHumiditySensor, matrixio_cpp_hal.PyHumidityData)
        self.update()

    def update(self):
        super(Humidity, self)._update_sensor()
        self.humidity = self._data.humidity
        self.temperature = self._data.temperature

