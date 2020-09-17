from setuptools import setup
from Cython.Build import cythonize

setup(
    # ext_modules=cythonize("numpy_cython_loop.pyx")
    # ext_modules=cythonize("cython_loop.pyx")
    ext_modules=cythonize("cython_loop_c_array.pyx")
)