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


class TestEvn(unittest.TestCase):
    def setUp(self):
        self._env = os.environ.get("DCLOADER_TEST_NODE")
        os.environ["DCLOADER_TEST_NODE"] = "10s"

    def tearDown(self):
        if self._env:
            os.environ["DCLOADER_TEST_NODE"] = self._env

    def test_timedelta(self):

        @dataclass
        class Root:
            node: timedelta

        loader = Loader([EnvSource("DCLOADER_TEST")])

        obj = loader.load(Root)

        self.assertEqual(obj.node, timedelta(seconds=10))
