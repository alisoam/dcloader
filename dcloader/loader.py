import abc
from dataclasses import MISSING, Field, dataclass, fields, is_dataclass
from typing import Any, TypeAlias, TypeVar

Path: TypeAlias = list[str]

T = TypeVar('T')


class Source(abc.ABC):
    @abc.abstractmethod
    def get(self, path: Path, value_type: type[T]) -> T | None:
        ...

    @abc.abstractmethod
    def exists(self, path: Path) -> bool:
        ...

    def __contains__(self, path: Path) -> bool:
        return self.exists(path)


@dataclass
class FieldValue:
    valid: bool = False
    value: Any = None


class Loader:
    def __init__(self, sources: list[Source]):
        self.sources = sources

    def _load(self, cls: type[T], path: Path = []) -> T | None:
        for source in self.sources:
            if path in source:
                break
        else:
            if path:
                return None

        params: dict[str, Any] = {}
        for field in fields(cls):
            if not field.init:
                continue

            field_vlaue = self._load_field(path, field)
            if field_vlaue.valid:
                params[field.name] = field_vlaue.value

        return cls(**params)

    def _load_field(self, base_path: Path, field: Field) -> FieldValue:
        field_path = base_path + [field.name]

        if is_dataclass(field.type):
            value = self._load(field.type, path=field_path)
            if value is not None:
                return FieldValue(value=value, valid=True)
        else:
            for source in self.sources:
                if field_path not in source:
                    continue

                return FieldValue(value=source.get(field_path, field.type), valid=True)

        if field.default is not MISSING:
            return FieldValue(value=field.default, valid=True)

        if field.default_factory is not MISSING:
            return FieldValue(value=field.default_factory(), valid=True)

        return FieldValue(valid=False)

    def load(self, cls: type[T]) -> T:
        value = self._load(cls)
        assert value is not None
        return value
