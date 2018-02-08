from matrixio_hal import bus

# device
print('Your device is a Matrix: {}'.format(bus.MATRIX_DEVICE))

# mcu firemware info
print('\nMCU:')
print('IDENTIFY = {}'.format(bus.MCU_IDENTIFY))
print('VERSION  = {}'.format(bus.MCU_FIRMWARE_VERSION))

# fpga firmware info
print('\nFPGA:')
print('IDENTIFY = {}'.format(bus.FPGA_IDENTIFY))
print('VERSION  = {}'.format(bus.FPGA_FIRMWARE_VERSION))

