from typing import TypeVar

import yaml
from dcloader.loader import Path, Source

from .utils import from_str

T = TypeVar("T")


class YAMLSource(Source):
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self.values = yaml.safe_load(file)

    def get(self, path: Path, value_type: type[T]) -> T:
        value = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                raise ValueError()

        if type(value) is str:
            return from_str(value, value_type)

        return value
