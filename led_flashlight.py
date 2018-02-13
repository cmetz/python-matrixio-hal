from matrixio_hal import everloop

# preserve the everloop on exit
everloop.atexit_clear_everloop = False

# create image with the proteced _flashslight color_name and render it
img = everloop.Image(init_color_name='_flashlight')
img.render()
print('Lights on!')
