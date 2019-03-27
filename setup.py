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
    version='1.1.0',

    description='A Python wrapper for Edison Sift API',
    long_description=long_description,

    url='http://developer.edison.tech',

    author='Edison',
    author_email='developer@edison.tech',
    license='MIT',

    keywords='email easilydo sift',

    packages=['siftapi'],

    install_requires=[
        'requests',
    ],
    test_suite='nose.collector',
    tests_require=['nose']
)

