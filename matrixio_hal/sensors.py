from . import bus
import abc

class BaseSensor:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self):
        pass
    
    def _read_sensor(self, address, unpack_format): 
        return bus.read(address, unpack_format)

class IMU(BaseSensor):
    def __init__(self):
        self._address = bus.IMU_ADR
        self._unpack_format = bus.IMU_UNPACK_FORMAT
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
        self.update()

    def update(self):
        self.yaw, \
        self.pitch, \
        self.roll, \
        self.accel_x, \
        self.accel_y, \
        self.accel_z, \
        self.gyro_x, \
        self.gyro_y, \
        self.gyro_z, \
        self.mag_x, \
        self.mag_y, \
        self.mag_z = super(IMU, self)._read_sensor(self._address, self._unpack_format)

class Pressure(BaseSensor):
    def __init__(self):
        self._address = bus.PRESSURE_ADR
        self._unpack_format = bus.PRESSURE_UNPACK_FORMAT
        self.altitude = 0.0
        self.pressure = 0.0
        self.temperature = 0.0
        self.update()

    def update(self):
        self.altitude, \
        self.pressure, \
        self.temperature = super(Pressure, self)._read_sensor(self._address, self._unpack_format)


class UV(BaseSensor):
    def __init__(self):
        self._address = bus.UV_ADR
        self._unpack_format = bus.UV_UNPACK_FORMAT
        self.uv = 0.0
        self.update()

    def update(self):
        self.uv = super(UV, self)._read_sensor(self._address, self._unpack_format)[0]

class Humidity(BaseSensor):
    def __init__(self):
        self._address = bus.HUMIDITY_ADR
        self._unpack_format = bus.HUMIDITY_UNPACK_FORMAT
        self.humidity = 0.0
        self.temperature = 0.0
        self.update()

    def update(self):
        self.humidity, \
        self.temperature = super(Humidity, self)._read_sensor(self._address, self._unpack_format)

