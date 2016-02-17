import os
from unittest import TestCase
import siftapi

from .sensitive import API_KEY, API_SECRET

here = os.path.dirname(os.path.realpath(__file__))

class TestDiscovery(TestCase):
    def _setup(self):
        self.sift = siftapi.Sift(API_KEY, API_SECRET)
        r = self.sift.discovery('%s/test.eml' % here)
        return r

    def _teardown(self):
        self.sift.remove_user('test')

    def test_is_200(self):
        r = self._setup()
        self.assertTrue(r['code'] == 200)
        self._teardown()

    def test_message_success(self):
        r = self._setup()
        self.assertTrue(r['message'] == 'OK')

