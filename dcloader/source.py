import os
from typing import Any

import yaml

from .loader import Path, Source


class DictSource(Source):
    def __init__(self, values: dict):
        self.values = values

    def get(self, path: Path, value_type: type) -> Any:
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


class YAMLSource(DictSource):
    def __init__(self, path: str):
        with open(path, 'r') as file:
            values = yaml.safe_load(file)
            super().__init__(values=values)


class EnvSource(Source):
    def __init__(self, prefix: str):
        self.prefix = prefix

    def get(self, path: Path, value_type: type) -> str | None:
        name = self.prefix + "_"
        name += "__".join(map(lambda x: x.upper(), path))
        value = os.environ.get(name)
        if value is None:
            return None
        return value_type(value)
