from typing import Any, TypeVar

from dcloader.loader import Path, Source

T = TypeVar("T")


class DictSource(Source):
    def __init__(self, values: dict):
        self.values = values

    def get(self, path: Path, value_type: type[T]) -> T:
        value: Any = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                raise ValueError()

        return value
