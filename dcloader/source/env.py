import os
from typing import TypeVar

from dcloader.loader import Path, Source

from .utils import from_str


T = TypeVar("T")

class EnvSource(Source):
    def __init__(self, prefix: str):
        self.prefix = prefix

    def get(self, path: Path, value_type: type[T]) -> T:
        name = self.name(path)
        value = os.environ.get(name)
        if value is None:
            raise ValueError()

        return from_str(value, value_type)

    def name(self, path: Path) -> str:
        name = self.prefix + "_"
        name += "__".join(map(lambda x: x.upper(), path))
        return name
