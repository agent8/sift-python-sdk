#!/usr/bin/env python
# coding=utf8

class APIError(Exception):
    def __init__(self, result):
        try:
            self.code = result['code']
        except:
            self.code = 500

        try:
            self.message = result['message']
        except:
            self.message = 'Server error'

        Exception.__init__(self, self.message)
