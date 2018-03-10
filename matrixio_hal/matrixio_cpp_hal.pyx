from libcpp cimport bool
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.stdint cimport uint16_t, uint32_t
from libcpp.vector cimport vector
from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as incr

cdef extern from "matrix_hal/wishbone_bus.h" namespace "matrix_hal":
    cdef cppclass WishboneBus:
        WishboneBus() except +
        bool SpiInit()
        bool SpiRead(uint16_t add, unsigned char* data, int length)
        void SpiClose()
        bool GetFPGAFrequency()
        uint32_t FPGAClock()

cdef extern from "matrix_hal/matrix_driver.h" namespace "matrix_hal":
    cdef cppclass MatrixDriver:
        MatrixDriver() except +
        void Setup(WishboneBus* wishbone)

cdef extern from "matrix_hal/fw_data.h" namespace "matrix_hal":
    cdef cppclass MCUData:
        uint32_t ID
        uint32_t version

cdef extern from "matrix_hal/mcu_firmware.h" namespace "matrix_hal":
    cdef cppclass MCUFirmware(MatrixDriver):
        MCUFirmware() except +
        bool Read(MCUData* data)

cdef extern from "matrix_hal/pressure_data.h" namespace "matrix_hal":
    cdef cppclass PressureData:
        float altitude
        float pressure
        float temperature

cdef extern from "matrix_hal/pressure_sensor.h" namespace "matrix_hal":
    cdef cppclass PressureSensor(MatrixDriver):
        PressureSensor() except +
        bool Read(PressureData* data)

cdef extern from "matrix_hal/humidity_data.h" namespace "matrix_hal":
    cdef cppclass HumidityData:
        float humidity
        float temperature

cdef extern from "matrix_hal/humidity_sensor.h" namespace "matrix_hal":
    cdef cppclass HumiditySensor(MatrixDriver):
        HumiditySensor() except +
        bool Read(HumidityData* data)

cdef extern from "matrix_hal/uv_data.h" namespace "matrix_hal":
    cdef cppclass UVData:
        float uv

cdef extern from "matrix_hal/uv_sensor.h" namespace "matrix_hal":
    cdef cppclass UVSensor(MatrixDriver):
        UVSensor() except +
        bool Read(UVData* data)

cdef extern from "matrix_hal/imu_data.h" namespace "matrix_hal":
    cdef cppclass IMUData:
        float yaw
        float pitch
        float roll
        float accel_x
        float accel_y
        float accel_z
        float gyro_x
        float gyro_y
        float gyro_z
        float mag_x
        float mag_y
        float mag_z

cdef extern from "matrix_hal/imu_sensor.h" namespace "matrix_hal":
    cdef cppclass IMUSensor(MatrixDriver):
        IMUSensor() except +
        bool Read(IMUData* data)

cdef extern from "matrix_hal/everloop_image.h" namespace "matrix_hal":
    const int kMatrixCreatorNLeds
    cdef cppclass LedValue:
        LedValue() except +
        uint32_t red
        uint32_t green
        uint32_t blue
        uint32_t white

    cdef cppclass EverloopImage:
        EverloopImage(int) except +
        vector[LedValue] leds

cdef extern from "matrix_hal/everloop.h" namespace "matrix_hal":
    cdef cppclass Everloop(MatrixDriver):
        Everloop() except +
        bool Write(const EverloopImage* led_image)

cdef extern from "matrix_hal/gpio_control.h" namespace "matrix_hal":
    cdef cppclass GPIOBank(MatrixDriver):
        GPIOBank() except +
        bool SetPeriod(uint16_t period)
        bool SetDuty(uint16_t channel, uint16_t duty)

    cdef cppclass GPIOControl:
        GPIOControl() except +
        void Setup(WishboneBus* bus)
        bool SetMode(uint16_t pin, uint16_t mode)
        bool SetFunction(uint16_t pin, uint16_t function)
        bool SetGPIOValue(uint16_t pin, uint16_t value)
        bool SetPrescaler(uint16_t bank, uint16_t prescaler)
        uint16_t GetGPIOValue(uint16_t pin)
        GPIOBank& Bank(uint16_t bank)
                

#
# Python Wrappers
#

cdef class PyReadData:
    cdef unsigned char* data
    cdef size_t size

    def __cinit__(self, size_t number):
        self.data = <unsigned char*> PyMem_Malloc(number * sizeof(unsigned char))
        self.size = number
    def __dealloc__(self):
        PyMem_Free(self.data)

    def get(self):
        return [self.data[i] for i in range(0, self.size)]

cdef class PyWishboneBus:
    cdef WishboneBus* thisptr
    def __cinit__(self):
        self.thisptr = new WishboneBus()
    def __dealloc__(self):
        del self.thisptr

    def SpiInit(self):
        return self.thisptr.SpiInit()

    def SpiRead(self, add, PyReadData data):
        return self.thisptr.SpiRead(add, data.data, data.size)

    def SpiClose(self):
        self.thisptr.SpiClose()

    def GetFPGAFrequency(self):
        return self.thisptr.GetFPGAFrequency()

    def FPGAClock(self):
        return self.thisptr.FPGAClock()

cdef class PyMatrixDriver:
    cdef MatrixDriver *driverptr
    def __cinit__(self):
        if type(self) is PyMatrixDriver:
            self.driverptr = new MatrixDriver()
    def __dealloc__(self):
        if type(self) is PyMatrixDriver:
            del self.driverptr

    def Setup(self, PyWishboneBus bus):
        self.driverptr.Setup(bus.thisptr)


cdef class PyMCUData:
    cdef MCUData* thisptr
    def __cinit__(self):
        self.thisptr = new MCUData()
    def __dealloc__(self):
        del self.thisptr

    @property
    def ID(self):
        return self.thisptr.ID

    @property
    def version(self):
        return self.thisptr.version

cdef class PyMCUFirmware(PyMatrixDriver):
    cdef MCUFirmware* thisptr
    def __cinit__(self):
        self.driverptr = self.thisptr = new MCUFirmware()
    def __dealloc__(self):
        del self.thisptr

    def Read(self, PyMCUData data):
        return self.thisptr.Read(data.thisptr)

cdef class PyPressureData:
    cdef PressureData* thisptr
    def __cinit__(self):
        self.thisptr = new PressureData()
    def __dealloc__(self):
        del self.thisptr

    @property
    def altitude(self):
        return self.thisptr.altitude

    @property
    def pressure(self):
        return self.thisptr.pressure

    @property
    def temperature(self):
        return self.thisptr.temperature

cdef class PyPressureSensor(PyMatrixDriver):
    cdef PressureSensor* thisptr
    def __cinit__(self):
        self.driverptr = self.thisptr = new PressureSensor()
    def __dealloc__(self):
        del self.thisptr

    def Read(self, PyPressureData data):
        return self.thisptr.Read(data.thisptr)
        
cdef class PyHumidityData:
    cdef HumidityData* thisptr
    def __cinit__(self):
        self.thisptr = new HumidityData()
    def __dealloc__(self):
        del self.thisptr

    @property
    def humidity(self):
        return self.thisptr.humidity

    @property
    def temperature(self):
        return self.thisptr.temperature

cdef class PyHumiditySensor(PyMatrixDriver):
    cdef HumiditySensor* thisptr
    def __cinit__(self):
        self.driverptr = self.thisptr = new HumiditySensor()
    def __dealloc__(self):
        del self.thisptr

    def Read(self, PyHumidityData data):
        return self.thisptr.Read(data.thisptr)

cdef class PyUVData:
    cdef UVData* thisptr
    def __cinit__(self):
        self.thisptr = new UVData()
    def __dealloc__(self):
        del self.thisptr

    @property
    def uv(self):
        return self.thisptr.uv

cdef class PyUVSensor(PyMatrixDriver):
    cdef UVSensor* thisptr
    def __cinit__(self):
        self.driverptr = self.thisptr = new UVSensor()
    def __dealloc__(self):
        del self.thisptr

    def Read(self, PyUVData data):
        return self.thisptr.Read(data.thisptr)

cdef class PyIMUData:
    cdef IMUData* thisptr
    def __cinit__(self):
        self.thisptr = new IMUData()
    def __dealloc__(self):
        del self.thisptr

    @property
    def yaw(self):
        return self.thisptr.yaw

    @property
    def pitch(self):
        return self.thisptr.pitch

    @property
    def roll(self):
        return self.thisptr.roll

    @property
    def accel_x(self):
        return self.thisptr.accel_x

    @property
    def accel_y(self):
        return self.thisptr.accel_y

    @property
    def accel_z(self):
        return self.thisptr.accel_z

    @property
    def gyro_x(self):
        return self.thisptr.gyro_x

    @property
    def gyro_y(self):
        return self.thisptr.gyro_y

    @property
    def gyro_z(self):
        return self.thisptr.gyro_z

    @property
    def mag_x(self):
        return self.thisptr.mag_x

    @property
    def mag_y(self):
        return self.thisptr.mag_y

    @property
    def mag_z(self):
        return self.thisptr.mag_z

cdef class PyIMUSensor(PyMatrixDriver):
    cdef IMUSensor* thisptr
    def __cinit__(self):
        self.driverptr = self.thisptr = new IMUSensor()
    def __dealloc__(self):
        del self.thisptr

    def Read(self, PyIMUData data):
        return self.thisptr.Read(data.thisptr)

cdef class PyLedValue:
    cdef LedValue* thisptr

    @property
    def red(self):
        return self.thisptr.red

    @red.setter
    def red(self, value):
        self.thisptr.red = value

    @property
    def green(self):
        return self.thisptr.green

    @green.setter
    def green(self, value):
        self.thisptr.green = value

    @property
    def blue(self):
        return self.thisptr.blue

    @blue.setter
    def blue(self, value):
        self.thisptr.blue = value

    @property
    def white(self):
        return self.thisptr.white

    @white.setter
    def white(self, value):
        self.thisptr.white = value

cdef class PyLeds:
    cdef vector[LedValue]* thisptr
    cdef vector[LedValue].iterator it

    def __len__(self):
        return self.thisptr.size()

    def __getitem__(self, index):
        led = PyLedValue()
        led.thisptr = &self.thisptr.at(index)
        return led

    def __iter__(self):
        self.it = self.thisptr.begin()
        return self

    def __next__(self):
        if self.it == self.thisptr.end():
            raise StopIteration()
        led = PyLedValue()
        led.thisptr = &deref(self.it)
        incr(self.it)
        return led

    def next(self):
        return self.__next__()

cdef class PyEverloopImage:
    cdef EverloopImage* thisptr
    def __cinit__(self, size=kMatrixCreatorNLeds):
        self.thisptr = new EverloopImage(size)
    def __dealloc__(self):
        del self.thisptr

    @property
    def leds(self):
        leds = PyLeds()
        leds.thisptr = &self.thisptr.leds
        return leds

cdef class PyEverloop(PyMatrixDriver):
    cdef Everloop* thisptr
    def __cinit__(self):
        self.driverptr = self.thisptr = new Everloop()
    def __dealloc__(self):
        del self.thisptr

    def Write(self, PyEverloopImage led_image):
        return self.thisptr.Write(led_image.thisptr)

cdef class PyGPIOControl:
    cdef GPIOControl* thisptr
    def __cinit__(self):
        self.thisptr = new GPIOControl()
    def __dealloc__(self):
        del self.thisptr

    def Setup(self, PyWishboneBus bus):
        self.thisptr.Setup(bus.thisptr)

    def SetMode(self, pin, mode):
        return self.thisptr.SetMode(pin, mode)

    def SetFunction(self, pin, function):
        return self.thisptr.SetFunction(pin, function)

    def SetGPIOValue(self, pin, value):
        return self.thisptr.SetGPIOValue(pin, value)

    def GetGPIOValue(self, pin):
        return self.thisptr.GetGPIOValue(pin)

    def SetPrescaler(self, bank, prescaler):
        return self.thisptr.SetPrescaler(bank, prescaler)

    def SetPeriod(self, bank, period):
        return self.thisptr.Bank(bank).SetPeriod(period)

    def SetDuty(self, bank, pin, duty):
        return self.thisptr.Bank(bank).SetDuty(pin, duty)

