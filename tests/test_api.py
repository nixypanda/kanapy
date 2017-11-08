import unittest
from kanapy.api import APIClient

class TestAPIClient(unittest.TestCase):

    def test_session_always_set(self):
        c = APIClient("testDomain", "testUser", "testPass")
        self.assertIsNotNone(c._session)

    def test_session_always_set_without_init(self):
        c = APIClient()
        self.assertIsNotNone(c._session)
