import os
from datetime import timedelta
from typing import Any, TypeVar, get_args, get_origin

import yaml

from .loader import Path, Source, ValueContainer
from .utils import str_to_timedelta

T = TypeVar("T")


class DictSource(Source):
    def __init__(self, values: dict):
        self.values = values

    def get(self, path: Path, value_type: type[T]) -> ValueContainer[T] | None:
        value: Any = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                return None

        return ValueContainer(value)


class YAMLSource(Source):
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self.values = yaml.safe_load(file)

    def get(self, path: Path, value_type: type[T]) -> ValueContainer[T] | None:
        value = self.values
        for key in path:
            value = value.get(key)
            if value is None:
                return None

        if value_type == timedelta:
            return ValueContainer(str_to_timedelta(value))  # type: ignore

        return ValueContainer(value)


class EnvSource(Source):
    def __init__(self, prefix: str):
        self.prefix = prefix

    def get(self, path: Path, value_type: type[T]) -> ValueContainer[T] | None:
        name = self.name(path)
        value = os.environ.get(name)
        if value is None:
            return None

        if get_origin(value_type) is list:
            return ValueContainer([get_args(value_type)[0](x) for x in value.split(",")])  # type: ignore

        if value_type == timedelta:
            return ValueContainer(str_to_timedelta(value))  # type: ignore

        return ValueContainer(value_type(value))  # type: ignore

    def name(self, path: Path) -> str:
        name = self.prefix + "_"
        name += "__".join(map(lambda x: x.upper(), path))
        return name
