from unittest import TestCase
import siftapi

from .sensitive import API_KEY, API_SECRET

class TestAddUser(TestCase):
    def _setup(self):
        self.sift = siftapi.Sift(API_KEY, API_SECRET)

    def _teardown(self):
        self.sift.remove_user('test')

    def test_is_200(self):
        self._setup()
        r = self.sift.add_user('test', 'en_US')
        self.assertTrue(r['code'] == 200)
        self._teardown()

    def test_result_username(self):
        self._setup()
        r = self.sift.add_user('test', 'en_US')
        self.assertTrue(r['result']['username'] == 'test')
        self._teardown()

    # TODO: Once an error is thrown for incorrect locale
    def test_incorrect_locale(self):
        pass
