import periphery
import struct

# Adresses
CONF_ADR = 0x0000
UART_ADR = 0x1000
MIC_ARRAY_ADR = 0x2000
EVERLOOP_ADR = 0x3000
GPIO_ADR = 0x4000
UV_ADR = 0x5000 + (0x00 >> 1)
PRESSURE_ADR = 0x5000 + (0x10 >> 1)
HUMIDITY_ADR = 0x5000 + (0x20 >> 1)
IMU_ADR = 0x5000 + (0x30 >> 1)
MCU_ADR = 0x5000 + (0x90 >> 1)

# Unpack formats
UV_UNPACK_FORMAT = 'f'
PRESSURE_UNPACK_FORMAT = 'f' * 3
HUMIDITY_UNPACK_FORMAT = 'ff' 
IMU_UNPACK_FORMAT = 'f' * 12
MCU_UNPACK_FORMAT = 'LL'

spi = periphery.SPI('/dev/spidev0.0', 3, 10000000)

def _transfer(adress, data):
    return spi.transfer([ord(b) for b in struct.pack('H', adress)] + data)

def write(adress, data):
    _transfer(adress << 1, data)

def read(adress, unpack_format):
    data = _transfer((adress << 1) + 1, [0] * struct.calcsize(unpack_format))
    return struct.unpack(unpack_format, bytearray(data[2:]))

