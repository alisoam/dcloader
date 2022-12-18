import os
import unittest
from dataclasses import dataclass
from datetime import timedelta

from dcloader import Loader
from dcloader.source import EnvSource


class TestEnv(unittest.TestCase):
    def test_bool(self):
        os.environ["DCLOADER_TEST_NODE"] = "true"
        @dataclass
        class Root:
            node: bool

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.node, True)


    def test_timedelta(self):
        os.environ["DCLOADER_TEST_NODE"] = "10s"
        @dataclass
        class Root:
            node: timedelta

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.node, timedelta(seconds=10))

    def test_nested(self):
        os.environ["DCLOADER_TEST_LEAF__NODE"] = "100"
        @dataclass
        class Leaf:
            node: int

        @dataclass
        class Root:
            leaf: Leaf

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.leaf.node, 100)

    def test_list(self):
        os.environ["DCLOADER_TEST_NODE"] = "1,2,3"
        @dataclass
        class Root:
            node: list[int]

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.node, [1, 2, 3])
