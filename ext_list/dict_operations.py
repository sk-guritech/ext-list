from __future__ import annotations

import copy
from types import FunctionType
from types import GetSetDescriptorType
from types import MethodDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import TypeVar

from ext_list import base

T = TypeVar('T')
TI = TypeVar('TI')
EXT_LIST = TypeVar('EXT_LIST', bound=type)


def to_dict(elements: list[T], key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, T]:
    if not elements:
        return {}

    get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(elements, key)

    return {get_value_method(element, key, *args): element for element in elements}


def to_dict_list(elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> list[dict[str | Hashable, T]]:
    def __to_dict_list_from_indexable_object(elements: list[T], keys: list[Hashable]) -> list[dict[str | Hashable, T]]:
        return [{key: element[key] for key in keys} for element in elements]   # type: ignore[attr-defined]

    def __to_dict_list_from_others(elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]]) -> list[dict[str | Hashable, T]]:
        if not arg_tuples:
            arg_tuples = list(tuple() for _ in range(len(keys)))

        result: list[dict[str | Hashable, T]] = []

        for element in elements:
            row: dict[str | Hashable, T] = __generate_dict_from_specified_keys(elements, keys, arg_tuples, element)

            result.append(row)

        return result

    def __generate_dict_from_specified_keys(
        elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]], element: T,
    ) -> dict[str | Hashable, Any]:
        result: dict[str | Hashable, Any] = {}

        for arg_tuple, key in zip(arg_tuples, keys):
            get_value_method = base.determine_get_value_method(elements, key)

            if isinstance(key, property):
                dict_key: str | Hashable = key.fget.__name__  # type: ignore[attr-defined]

            elif isinstance(key, FunctionType) or isinstance(key, MethodDescriptorType) or isinstance(key, GetSetDescriptorType):
                dict_key = key.__name__

            elif isinstance(key, str):
                dict_key = key

            else:
                dict_key = key

            result[dict_key] = get_value_method(element, key, *arg_tuple)  # type: ignore[assignment]

        return result

    if not elements:
        return []

    if base.is_indexable(elements):
        return __to_dict_list_from_indexable_object(elements, keys)

    return __to_dict_list_from_others(elements, keys, arg_tuples)


def to_dict_with_complex_keys(elements: list[T], keys: list[FunctionType | property | str] | list[Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> dict[tuple[Any, ...], T]:
    def __to_dict_with_complex_keys_from_indexable_object(elements: list[T], keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        return {tuple(element[key] for key in keys): element for element in elements}  # type: ignore[index]

    def __to_dict_with_complex_keys_from_others(elements: list[T], keys: list[FunctionType | property | str], arg_tuples: list[tuple[Any, ...]]) -> dict[tuple[Any, ...], T]:
        result: dict[tuple[Any, ...], T] = {}

        if not arg_tuples:
            arg_tuples = list(tuple() for _ in range(len(keys)))

        for element in elements:
            tupled_key: tuple[Any, ...] = __generate_tupled_key(elements, keys, element, arg_tuples)
            result[tupled_key] = element

        return result

    def __generate_tupled_key(elements: list[T], keys: list[FunctionType | property | str], element: T, arg_tuples: list[tuple[Any, ...]]) -> tuple[Any, ...]:
        tupled_key: tuple[Any, ...] = tuple()

        for key, arg_tuple in zip(keys, arg_tuples):
            get_value_method = base.determine_get_value_method(elements, key)
            tupled_key += (get_value_method(element, key, *arg_tuple),)

        return tupled_key

    if not elements:
        return {}

    if base.is_indexable(elements):
        return __to_dict_with_complex_keys_from_indexable_object(elements, keys)  # type: ignore[arg-type]

    return __to_dict_with_complex_keys_from_others(elements, keys, arg_tuples)  # type: ignore[arg-type]


def dicts_to_instances(elements: list[dict[str, Any]], type_: TI) -> list[TI]:
    return [type_(**element) for element in elements]  # type: ignore[assignment]


def group_by_key(ext_list_type: EXT_LIST, elements: list[T], key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, EXT_LIST]:
    result: dict[Hashable, EXT_LIST] = {}

    get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(elements, key)

    for element in elements:
        group_key: Hashable = get_value_method(element, key, *args)

        if group_key in result:
            result[group_key].append(element)  # type: ignore[attr-defined]

        else:
            result[group_key] = ext_list_type([element])  # type: ignore[attr-defined]

    return result


def rename_keys(elements: list[T], rename_keys: dict[Hashable, Hashable]) -> list[T]:
    if not elements:
        return []

    if not base.is_indexable(elements):
        raise TypeError

    result: list[T] = []

    for element in copy.deepcopy(elements):
        for from_key, to_key in rename_keys.items():
            element[to_key] = element.pop(from_key)  # type: ignore[attr-defined]

        result.append(element)  # type: ignore[assignment]

    return result
