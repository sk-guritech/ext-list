from __future__ import annotations

from types import GetSetDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterable
from typing import List
from typing import TypeVar

from ext_list import base
T = TypeVar('T')


class _ListOperation(List[T]):  # type: ignore
    def extract(self, key: Callable[[T, Any], Any] | property | str | Hashable, *args: Any) -> Iterable[Any]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element[key] for element in self])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([key(element, *args) for element in self])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([key.__get__(element) for element in self])

        raise KeyError

    def extract_duplicates(self, other: Iterable[T]) -> Iterable[T]:
        return self.__class__([element for element in self if element in other])

    def is_duplicate(self) -> bool:
        return (len(self) - len(set(self))) > 0

    def one(self) -> T | None:
        try:
            return self[0]

        except IndexError:
            return None

    def first(self) -> T:
        return self[0]

    def map(self, function: Callable[[T, Any], Any] | type, *args: Any) -> Iterable[Any]:
        return self.__class__([function(element, *args) for element in self])
