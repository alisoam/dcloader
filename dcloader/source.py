import os
from datetime import timedelta
from typing import TypeVar

import yaml

from .loader import Path, Source
from .utils import str_to_timedelta

T = TypeVar("T")


class DictSource(Source):
    def __init__(self, values: dict):
        self.values = values

    def get(self, path: Path, value_type: type[T]) -> T | None:
        value = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                return None

        assert isinstance(value, value_type)
        return value

    def exists(self, path: Path) -> bool:
        value = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                return False

        return True


class YAMLSource(Source):
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self.values = yaml.safe_load(file)

    def get(self, path: Path, value_type: type[T]) -> T | None:
        value = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                return None

        if value_type == timedelta:
            assert type(value) is str
            return str_to_timedelta(value)

        assert isinstance(value, value_type)
        return value

    def exists(self, path: Path) -> bool:
        if self.values is None:
            return False

        value = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                return False

        return True


class EnvSource(Source):
    def __init__(self, prefix: str):
        self.prefix = prefix

    def get(self, path: Path, value_type: type[T]) -> T | None:
        value = os.environ.get(self.name(path))
        if value is None:
            return None

        if value_type == timedelta:
            return str_to_timedelta(value)

        return value_type(value)

    def exists(self, path: Path) -> bool:
        return os.environ.get(self.name(path)) is not None

    def name(self, path: Path) -> str:
        name = self.prefix + "_"
        name += "__".join(map(lambda x: x.upper(), path))
        return name
