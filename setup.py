from setuptools import setup, Extension

ext = [Extension('matrixio_hal.matrixio_cpp_hal',
       ['matrixio_hal/matrixio_cpp_hal.pyx'],
       libraries=['matrix_creator_hal'],
       extra_compile_args=['-std=c++11'],
       language='c++')
      ]

setup(
      name='python-matrixio-hal',
      version='1.0.0',
      description='Python HAL for the Matrix Creator / Voice wrapping the C++ drivers',
      author='cmetz',
      author_email='christoph.metz@gulp.de',
      url='https://github.com/cmetz/python-matrixio-hal',
      license='MIT',
      packages=['matrixio_hal'],
      setup_requires=[
          'setuptools>=18.0',
          'cython'
          ],
      ext_modules=ext,
      zip_safe=False
    )
