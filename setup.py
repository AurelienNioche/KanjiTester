from distutils.core import setup
from Cython.Build import cythonize

from os import path

setup(
    ext_modules=cythonize(path.join("plugins", "visual_similarity", "metrics", "stroke.pyx"))
)
