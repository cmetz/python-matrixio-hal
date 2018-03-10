try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
try:
    from setuptools.extension import Extension
except ImportError:
    from distutils.extension import Extension
from Cython.Build import cythonize

sourcefiles = ['matrixio_hal/matrixio_cpp_hal.pyx']
compile_opts = ['-std=c++11']

ext = [Extension('*',
       sourcefiles,
       libraries=['matrix_creator_hal'],
       extra_compile_args=compile_opts,
       language='c++')
      ]

setup(
      name='python-matriox-hal',
      version='1.0.0',
      description='Python HAL for the Matrix Creator / Voice wrapping the C++ drivers',
      author='cmetz',
      url='https://github.com/cmetz/python-matrixio-hal',
      license='MIT',
      packages=['matrixio_hal'],
      install_requires=['Cython'],
      ext_modules=cythonize(ext),
      zip_safe=False
    )
