import os
import tempfile
import unittest
from dataclasses import dataclass
from datetime import timedelta

from dcloader import EnvSource, Loader, YAMLSource

timedelta_yaml = """
node: 10s
"""


class TestYaml(unittest.TestCase):
    def test_timedelta(self):
        @dataclass
        class Root:
            node: timedelta

        with tempfile.NamedTemporaryFile() as f:
            f.write(timedelta_yaml.encode("utf8"))
            f.flush()

            loader = Loader([YAMLSource(f.name)])

            obj = loader.load(Root)

            self.assertEqual(obj.node, timedelta(seconds=10))


class TestEnv(unittest.TestCase):
    def setUp(self):
        os.environ["DCLOADER_TEST_NODE"] = "10s"
        os.environ["DCLOADER_TEST_LEAF__NODE"] = "100"

    def test_timedelta(self):
        @dataclass
        class Root:
            node: timedelta

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.node, timedelta(seconds=10))

    def test_nested(self):

        @dataclass
        class Leaf:
            node: int

        @dataclass
        class Root:
            leaf: Leaf

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.leaf.node, 100)
