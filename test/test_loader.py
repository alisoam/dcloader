import unittest
from dataclasses import dataclass, field

from dcloader import DictSource, Loader


class Test(unittest.TestCase):
    def test(self):
        @dataclass
        class Root:
            node1: str
            node2: int

        loader = Loader([DictSource({"node1": "value", "node2": 1})])

        obj = loader.load(Root)

        self.assertEqual(obj.node1, "value")
        self.assertEqual(obj.node2, 1)


class TestDataclass(unittest.TestCase):
    def test_init(self):
        @dataclass
        class Root:
            node1: str
            node2: str = field(init=False)

        loader = Loader([DictSource({"node1": "value"})])

        obj = loader.load(Root)

        self.assertEqual(obj.node1, "value")

    def test_default(self):
        @dataclass
        class Root:
            node1: str = "default"
            node2: str = field(default="default")

        loader = Loader([])

        obj = loader.load(Root)

        self.assertEqual(obj.node1, "default")
        self.assertEqual(obj.node2, "default")

    def test_default_factory(self):
        @dataclass
        class Leaf:
            node: str = "default"

        @dataclass
        class Root:
            node: Leaf = field(default_factory=lambda: Leaf(node="value"))

        loader = Loader([])

        obj = loader.load(Root)

        self.assertEqual(obj.node.node, "value")

    def test_union(self):
        @dataclass
        class Root:
            node1: str | int

        loader1 = Loader([DictSource({"node1": "value"})])
        loader2 = Loader([DictSource({"node1": 1})])

        obj1 = loader1.load(Root)
        obj2 = loader2.load(Root)

        self.assertEqual(obj1.node1, "value")
        self.assertEqual(obj2.node1, 1)
