#!/usr/bin/env python
# coding=utf8

from . import version

VERSION = version.__version__
API_URL = "https://api.easilydo.com"

def build_url(path):
    return '%s/%s%s' % (API_URL, VERSION, path)

