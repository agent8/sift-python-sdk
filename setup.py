#!/usr/bin/env python
# coding=utf8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='siftapi',
    version='1.0.6',

    description='A Python wrapper for EasilyDo\'s Sift API',
    long_description=long_description,

    url='http://sift.easilydo.com',

    author='EasilyDo',
    author_email='production@easilydo.com',
    license='MIT',

    keywords='email easilydo sift',

    packages=['siftapi'],

    install_requires=[
        'requests',
    ],
    test_suite='nose.collector',
    tests_require=['nose']
)

