from matrixio_hal import bus

# mcu firemware info
print('MCU:')
print('IDENTIFY = {}'.format(bus.MCU_FIRMWARE_IDENTIFY))
print('VERSION  = {}'.format(bus.MCU_FIRMWARE_VERSION))

# fpga firmware info
print('\nFPGA:')
print('IDENTIFY = {}'.format(bus.FPGA_FIRMWARE_IDENTIFY))
print('VERSION  = {}'.format(bus.FPGA_FIRMWARE_VERSION))

