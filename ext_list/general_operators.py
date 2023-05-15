from __future__ import annotations

from types import FunctionType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import TypeVar

from ext_list import base
T = TypeVar('T')


def equal(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value is compare_target or value == compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def not_equal(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value is not compare_target and value != compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def greater(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value > compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def greater_or_equal(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value >= compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def less(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value < compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def less_or_equal(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value <= compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def in_(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value in compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def not_in_(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> list[T]:
    def __operator(value: Any, compare_target: Any) -> bool:
        return value not in compare_target

    return __operator_base(elements, key, compare_target, __operator, *args)


def __operator_base(elements: list[T], key: FunctionType | property | str | Hashable, compare_target: Any, operator: Callable[[Any, Any], bool], *args: Any) -> list[T]:
    if not elements:
        return []

    get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(elements, key)

    return [element for element in elements if operator(get_value_method(element, key, *args), compare_target)]
