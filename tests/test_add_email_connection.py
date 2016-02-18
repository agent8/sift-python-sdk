from unittest import TestCase
import siftapi

from .sensitive import API_KEY, API_SECRET

class TestAddEmailConnection(TestCase):
    def _setup(self):
        self.sift = siftapi.Sift(API_KEY, API_SECRET)
        self.sift.add_user('test', 'en_US')

    def _teardown(self):
        self.sift.remove_user('test')

    def test_raises_error(self):
        self._setup()
        self.assertRaises(Exception, self.sift.add_email_connection, 'test', None)
        self._teardown()
