import abc
import types
from dataclasses import MISSING, fields, is_dataclass
from typing import Any, TypeAlias, TypeVar, get_args, get_origin

Path: TypeAlias = list[str]

T = TypeVar('T')


class Source(abc.ABC):
    @abc.abstractmethod
    def get(self, path: Path, value_type: type[T]) -> T:
        ...


class Loader:
    def __init__(self, sources: list[Source]):
        self.sources = sources

    def _load(self, cls: type[T], path: Path = []) -> T:
        if is_dataclass(cls):
            return self.load_dataclass(cls, path)

        return self.load_others(cls, path)


    def load_dataclass(self, cls: type[T], path: Path) -> T:
        params: dict[str, Any] = {}
        has_non_default = False

        for field in fields(cls):
            if not field.init:
                continue

            field_path = path + [field.name]

            try:
                params[field.name] = self._load(field.type, path=field_path)
                has_non_default = True
            except ValueError:
                pass

            if field.name in params:
                continue

            if field.default is not MISSING:
                params[field.name] = field.default

            if field.default_factory is not MISSING:
                params[field.name] = field.default_factory()

        if not has_non_default and path:
            raise ValueError()

        return cls(**params)

    def load_union(self, types: tuple[type, ...], path: Path) -> Any:
        for field_type in types:
            try:
                return self._load(field_type, path=path)
            except ValueError:
                pass

        raise ValueError()

    def load_others(self, cls: type[T], path: Path) -> T:
        if get_origin(cls) is types.UnionType:
            return self.load_union(get_args(cls), path)

        for source in self.sources:
            try:
                return source.get(path=path, value_type=cls)
            except ValueError:
                pass

        raise ValueError()

    def load(self, cls: type[T]) -> T:
        return self._load(cls)
