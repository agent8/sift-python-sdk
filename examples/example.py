#!/usr/bin/env python
# coding=utf8

import siftapi

# Get your API Key and Secret from the Sift Dashboard at sift.easilydo.com
API_KEY = ''
API_SECRET = ''

sift = siftapi.Sift(API_KEY, API_SECRET)

# Add a new user
print 'Example: Add user'
sift.add_user('test')

# Email Discovery
print 'Example: Discovery'
sift.discovery('test.eml')

print 'Example: Get Sifts'
sift.get_sifts('xbili')

print 'Example: Get Token'
sift.get_token('xbili')

print 'Example: Remove user'
sift.remove_user('test')

