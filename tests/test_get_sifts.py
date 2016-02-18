import os
from unittest import TestCase
import siftapi

from .sensitive import API_KEY, API_SECRET

here = os.path.dirname(os.path.realpath(__file__))

class TestGetSifts(TestCase):
    def _setup(self):
        self.sift = siftapi.Sift(API_KEY, API_SECRET)
        self.sift.add_user('test', 'en_US')
        return

    def _teardown(self):
        self.sift.remove_user('test')
        return

    def test_is_200(self):
        self._setup()
        r = self.sift.get_sifts('test')
        self.assertTrue(r['code'] == 200)
        self._teardown()
        return

    def test_optional_variables(self):
        self._setup()
        r = self.sift.get_sifts('test', limit=1)
        self.assertTrue(len(r['result']) <= 1)
        return

    def test_message_success(self):
        self._setup()
        r = self.sift.get_sifts('test')
        self.assertTrue(r['message'] == 'success')
        self._teardown()
        return

    def test_response_content(self):
        self._setup()
        r = self.sift.get_sifts('test')
        self.assertTrue(isinstance(r['result'], list))
        self._teardown()
        return

