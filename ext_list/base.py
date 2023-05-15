from __future__ import annotations

from types import FunctionType
from types import GetSetDescriptorType
from types import MethodDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import TypeVar

T = TypeVar('T')


def determine_get_value_method(elements: list[T], key: FunctionType | property | str | Hashable) -> Callable[[T, Any], Any]:
    def __get_value_by_function(element: T, func: FunctionType, *args: Any) -> Any:
        return func(element, *args)

    def __get_value_by_index(element: T, index: Hashable | Hashable, *args: Any) -> Any:
        return element[index]  # type: ignore

    def __get_value_by_property(element: T, prop: property, *args: Any) -> Any:
        return prop.__get__(element)  # type: ignore[misc]

    def __get_value_by_attr_name(element: T, attr_name: str, *args: Any) -> Any:
        value = getattr(element, attr_name)

        if callable(value):
            return value(*args)

        return value

    if is_indexable(elements):
        return __get_value_by_index

    if isinstance(key, FunctionType) or isinstance(key, MethodDescriptorType):
        return __get_value_by_function

    if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
        return __get_value_by_property

    return __get_value_by_attr_name


def is_indexable(elements: list[Any]) -> bool:
    return all(hasattr(element, '__getitem__') for element in elements)
