import unittest
from dataclasses import dataclass, field

from dcloader import Loader
from dcloader.source import DictSource


class Test(unittest.TestCase):
    def test(self):
        @dataclass
        class Root:
            node1: str
            node2: int
            node3: float

        loader = Loader([DictSource({"node1": "value", "node2": 1, "node3": 1.5})])

        obj = loader.load(Root)

        self.assertEqual(obj.node1, "value")
        self.assertEqual(obj.node2, 1)
        self.assertEqual(obj.node3, 1.5)


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
            node1: str = "default-1"
            node2: str = field(default="default-2")
            node3: str = "default-3"
            node4: str = field(default="default-4")

        loader = Loader([DictSource({"node3": "non-default-1", "node4": "non-default-2"})])

        obj = loader.load(Root)

        self.assertEqual(obj.node1, "default-1")
        self.assertEqual(obj.node2, "default-2")
        self.assertEqual(obj.node3, "non-default-1")
        self.assertEqual(obj.node4, "non-default-2")

    def test_default_factory(self):
        @dataclass
        class Leaf:
            node: str = "default"

        @dataclass
        class Root:
            leaf: Leaf = field(default_factory=lambda: Leaf(node="value"))

        loader = Loader([])

        obj = loader.load(Root)

        self.assertEqual(obj.leaf.node, "value")

    def test_union(self):
        @dataclass
        class Leaf:
            node: str = "default"

        @dataclass
        class Root:
            node1: str | Leaf

        loader1 = Loader([DictSource({"node1": "value"})])
        loader2 = Loader([DictSource({"node1": Leaf("value")})])

        obj1 = loader1.load(Root)
        obj2 = loader2.load(Root)

        self.assertEqual(obj1.node1, "value")
        self.assertEqual(obj2.node1, Leaf("value"))
