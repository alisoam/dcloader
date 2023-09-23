import unittest
from datetime import timedelta

from dcloader.source.utils import from_str


class TestFromStr(unittest.TestCase):
    def test_primitives(self):
        self.assertEqual(from_str("1234", int), 1234)
        self.assertEqual(from_str("1.234", float), 1.234)
        self.assertEqual(from_str("1234", str), "1234")
        self.assertEqual(from_str("false", bool),  False)

    def test_list(self):
        self.assertEqual(from_str("1234", list[int]), [1234])
        self.assertEqual(from_str("1234,5678", list[int]), [1234, 5678])

    def test_timedelta(self):
        self.assertEqual(from_str("12s", timedelta), timedelta(seconds=12))
