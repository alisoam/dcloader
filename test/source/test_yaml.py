import tempfile
import unittest
from dataclasses import dataclass
from datetime import timedelta

from dcloader import Loader
from dcloader.source import YAMLSource

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
