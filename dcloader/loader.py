import abc
from dataclasses import MISSING, dataclass, fields, is_dataclass
from typing import Any, Generic, TypeAlias, TypeVar

Path: TypeAlias = list[str]

T = TypeVar('T')


@dataclass
class ValueContainer(Generic[T]):
    value: T


class Source(abc.ABC):
    @abc.abstractmethod
    def get(self, path: Path, value_type: type[T]) -> ValueContainer[T] | None:
        ...


class Loader:
    def __init__(self, sources: list[Source]):
        self.sources = sources

    def _load(self, cls: type[T], path: Path = []) -> T | None:
        params: dict[str, Any] = {}
        has_non_default = False
        for field in fields(cls):
            if not field.init:
                continue

            field_path = path + [field.name]

            if is_dataclass(field.type):
                v = self._load(field.type, path=field_path)
                if v is not None:
                    params[field.name] = v
                    has_non_default = True
            else:
                for source in self.sources:
                    v = source.get(path=field_path, value_type=field.type)
                    if v is None:
                        continue

                    params[field.name] = v.value
                    has_non_default = True

            if field.default is not MISSING:
                params[field.name] = field.default

            if field.default_factory is not MISSING:
                params[field.name] = field.default_factory()

        if not has_non_default and path:
            return None

        return cls(**params)

    def load(self, cls: type[T]) -> T:
        value = self._load(cls)
        assert value is not None
        return value
