#!/usr/bin/env python

from distutils.core import setup

try:  # Python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2.x
    from distutils.command.build_py import build_py

setup(name='python-montage',
      version='0.9.3',
      description='python-montage - a python Montage wrapper',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      url='http://astrofrog.github.com/python-montage/',
      packages=['montage'],
      provides=['montage'],
      cmdclass={'build_py': build_py},
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
