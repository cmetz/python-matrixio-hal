from matrixio_hal import everloop

# atext_clear_everloop can be set to False
# so we do not clear twice
everloop.atexit_clear_everloop = False
# render empty image
everloop.Image().render()
print('Leds cleared.')
