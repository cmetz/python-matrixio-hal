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
MCU_INFO_UNPACK_FORMAT = 'LL'
FPGA_INFO_UNPACK_FORMAT = 'LL'

spi = periphery.SPI('/dev/spidev0.0', 3, 10000000)

def _transfer(address, data):
    return spi.transfer([ord(b) for b in struct.pack('H', address)] + data)

def write(address, data):
    _transfer(address << 1, data)

def read(address, unpack_format):
    data = _transfer((address << 1) + 1, [0] * struct.calcsize(unpack_format))
    return struct.unpack(unpack_format, bytearray(data[2:]))

# set some infos about the MCU and FPGA
MCU_FIRMWARE_IDENTIFY, MCU_FIRMWARE_VERSION = ['{:x}'.format(d) for d in read(MCU_ADR, MCU_INFO_UNPACK_FORMAT)]
FPGA_FIRMWARE_IDENTIFY, FPGA_FIRMWARE_VERSION = ['{:x}'.format(d) for d in read(CONF_ADR, FPGA_INFO_UNPACK_FORMAT)]

