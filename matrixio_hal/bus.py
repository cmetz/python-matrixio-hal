import periphery
import struct
import signal
import sys

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

debug = False

# handle SIGTERM as normal sys.exit()
# e.g. docker stop send SIGTERM by default
def sigterm_handler(signal, frame):
    sys.exit()

signal.signal(signal.SIGTERM, sigterm_handler)


spi = periphery.SPI('/dev/spidev0.0', 3, 10000000)

def _transfer(address, data):
    if sys.version_info[0] == 2:
        if debug:
            print(['{:x}'.format(ord(b)) for b in struct.pack('H', address)] + data)
        return spi.transfer([ord(b) for b in struct.pack('H', address)] + data)
    else:
        if debug:
            print(['{:x}'.format(b) for b in struct.pack('H', address)] + data)
        return spi.transfer(struct.pack('H', address) + bytearray(data)) 

def write(address, data):
    _transfer(address << 1, data)

def read(address, unpack_format):
    data = _transfer((address << 1) + 1, [0] * struct.calcsize(unpack_format))
    return struct.unpack(unpack_format, bytearray(data[2:]))


# set some infos about the MCU and FPGA
MCU_IDENTIFY, MCU_FIRMWARE_VERSION = ['{:x}'.format(d) for d in read(MCU_ADR, MCU_INFO_UNPACK_FORMAT)]
FPGA_IDENTIFY, FPGA_FIRMWARE_VERSION = ['{:x}'.format(d) for d in read(CONF_ADR, FPGA_INFO_UNPACK_FORMAT)]

MATRIX_DEVICE = 'unknown'
if FPGA_IDENTIFY == '5c344e8':
    MATRIX_DEVICE = 'creator'
elif FPGA_IDENTIFY == '6032bad2':
    MATRIX_DEVICE = 'voice'

