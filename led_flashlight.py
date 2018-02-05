from matrixio_hal import everloop

# create image with the proteced _flashslight color_name and render it
img = everloop.Image(init_color_name='_flashlight')
img.render()
print('Lights on!')
