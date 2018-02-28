import matrixio_hal

BANK = 0
SERVO_PIN = 0
PRESCALER = 0x5

bus = matrixio_hal.WishboneBus()
bus.SpiInit()

gpio = matrixio_hal.GPIOControl()
gpio.Setup(bus)

gpio.SetMode(SERVO_PIN, 1)
gpio.SetFunction(SERVO_PIN, 1)
gpio.SetPrescaler(BANK, PRESCALER)

PWM_PERIOD = 1.0 / 38000
FPGA_CLOCK = 125000000

period_counter = int(PWM_PERIOD * FPGA_CLOCK // ((1 << PRESCALER) *2))

bank = gpio.Bank(BANK)
bank.SetPeriod(period_counter)
bank.SetDuty(SERVO_PIN, 0)
