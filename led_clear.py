from matrixio_hal import everloop

# just use the atexit callback in everloop to clear the everloop
# atext_clear_everloop is True by default, but we set it for demonstration
everloop.atexit_clear_everloop = True
print('Leds cleared.')
