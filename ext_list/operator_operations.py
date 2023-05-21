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


class _OperatorOperation(List[T]):  # type: ignore
    def equal(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] == compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) == compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) == compare_target])

        raise KeyError

    def not_equal(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] != compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) != compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) != compare_target])

        raise KeyError

    def greater(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] > compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) > compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) > compare_target])

        raise KeyError

    def greater_or_equal(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] >= compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) >= compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) >= compare_target])

        raise KeyError

    def less(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] < compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) < compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) < compare_target])

        raise KeyError

    def less_or_equal(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] <= compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) <= compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) <= compare_target])

        raise KeyError

    def in_(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] in compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) in compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) in compare_target])

        raise KeyError

    def not_in_(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> Iterable[T]:
        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__([element for element in self if element[key] not in compare_target])  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return self.__class__([element for element in self if key(element, *args) not in compare_target])

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return self.__class__([element for element in self if key.__get__(element) not in compare_target])

        raise KeyError
