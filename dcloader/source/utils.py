import builtins
import types
from datetime import timedelta
from typing import Any, get_origin, get_args


def timedelta_from_str(duration: str) -> timedelta:
    if duration.endswith("s"):
        return timedelta(seconds=int(duration[:-1]))

    if duration.endswith("m"):
        return timedelta(minutes=int(duration[:-1]))

    if duration.endswith("h"):
        return timedelta(hours=int(duration[:-1]))

    if duration.endswith("d"):
        return timedelta(days=int(duration[:-1]))

    raise ValueError("not supported")


def from_str(value: str, t) -> Any:
    if t in (str, int, float, bool):
        return t(value)

    if t is timedelta:
        return timedelta_from_str(value)

    if get_origin(t) is builtins.list:
        item_type = next(iter(get_args(t)), str)
        return list(from_str(v, item_type) for v in value.split(","))

    if value is None and t is None:
        return None

    raise ValueError
