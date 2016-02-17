from unittest import TestCase
import siftapi

from .sensitive import API_KEY, API_SECRET

class TestAddUser(TestCase):
    def _setup(self):
        self.sift = siftapi.Sift(API_KEY, API_SECRET)
        r = self.sift.add_user('test')
        return r

    def _teardown(self):
        self.sift.remove_user('test')

    def test_is_200(self):
        r = self._setup()
        self.assertTrue(r['code'] == 200)
        self._teardown()

    def test_result_username(self):
        r = self._setup()
        self.assertTrue(r['result']['username'] == 'test')
        self._teardown()

