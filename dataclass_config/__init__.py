import os
from dataclasses import fields, is_dataclass
from typing import Any

import yaml


def _load(cls: type, values: dict | None = None, prefix: list[str] = []):
    params: dict[str, Any] = {}
    for field in fields(cls):
        field_prefix = prefix + [field.name.upper()]
        field_env_prefix = "_".join(map(lambda p: p.upper(), field_prefix))
        env_value = os.environ.get(field_env_prefix)

        value = None
        if is_dataclass(field.type):
            field_values = values.get(field.name) if values else None
            value = _load(field.type, values=field_values, prefix=field_prefix)
        elif env_value:
            value = field.type(env_value)
        elif values:
            value = values.get(field.name)

        if value:
            params[field.name] = value

    return cls(**params)


def load(cls: type, path: str | None= None, prefix: str = ""):
    values = None
    if path:
        with open(path, 'r') as file:
            values = yaml.safe_load(file)

    return _load(cls, values=values, prefix=[prefix])
