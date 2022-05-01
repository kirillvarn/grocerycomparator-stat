from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="cython app",
    ext_modules=cythonize("cor.pyx"),
    zip_safe=False,
    include_dirs=[numpy.get_include()]
)