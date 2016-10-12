#!/usr/bin/env python
# coding=utf8

from . import version

VERSION = version.__version__
API_URL = {
    'production': "https://api.easilydo.com",
    'engineering': "https://api-engineering.easilydo.com",
}

def build_url(env, path):
    url = API_URL[env]
    return '%s/%s%s' % (url, VERSION, path)
