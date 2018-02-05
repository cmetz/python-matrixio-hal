from collections import namedtuple
from matrixio_hal import bus

# mcu firemware info
Info = namedtuple('Info', 'fid version')
info = Info._make(bus.read(bus.MCU_ADR, bus.MCU_UNPACK_FORMAT))
print('Firmware id: 0x{:x}'.format(info.fid))
print('Version: 0x{:x}'.format(info.version))

