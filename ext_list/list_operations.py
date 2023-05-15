from __future__ import annotations

import copy
from types import FunctionType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import TypeVar

from ext_list import base
T = TypeVar('T')


def extract(elements: list[T], key: FunctionType | property | str | Hashable, *args: Any) -> list[Any]:
    if not elements:
        return []

    get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(elements, key)

    return [get_value_method(element, key, *args) for element in elements]  # type: ignore[arg-type]


def extract_duplicates(elements: list[T], other: list[T]) -> list[T]:
    return [element for element in elements if element in other]


def is_duplicate(elements: list[T]) -> bool:
    if not elements:
        return False

    tmp_ext_list: list[T] = copy.deepcopy(elements)

    for _ in range(len(tmp_ext_list)):
        if tmp_ext_list.pop() in tmp_ext_list:
            return True

    return False


def one(elements: list[T]) -> T | None:
    try:
        return elements[0]

    except IndexError:
        return None


def first(elements: list[T]) -> T:
    return elements[0]
