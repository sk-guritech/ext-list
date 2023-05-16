from __future__ import annotations

import copy
from types import FunctionType
from types import GetSetDescriptorType
from types import MethodDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import List
from typing import TypeVar

from ext_list import base

T = TypeVar('T')
TI = TypeVar('TI')


class _DictOperation(List[T]):
    def to_dict(self, key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, T]:
        if not self:
            return {}

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        return {get_value_method(element, key, *args): element for element in self}

    def to_dict_list(self, keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> _DictOperation[dict[str | Hashable, T]]:
        def __to_dict_list_from_indexable_object(elements: list[T], keys: list[Hashable]) -> _DictOperation[dict[str | Hashable, T]]:
            return _DictOperation([{key: element[key] for key in keys} for element in elements])   # type: ignore[attr-defined]

        def __to_dict_list_from_others(
            elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]],
        ) -> _DictOperation[dict[str | Hashable, T]]:
            if not arg_tuples:
                arg_tuples = list(tuple() for _ in range(len(keys)))

            result: _DictOperation[dict[str | Hashable, T]] = _DictOperation()

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

        if not self:
            return _DictOperation()

        if base.is_indexable(self):
            return __to_dict_list_from_indexable_object(self, keys)

        return __to_dict_list_from_others(self, keys, arg_tuples)

    def to_dict_with_complex_keys(self, keys: list[FunctionType | property | str] | list[Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> dict[tuple[Any, ...], T]:
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

        if not self:
            return {}

        if base.is_indexable(self):
            return __to_dict_with_complex_keys_from_indexable_object(self, keys)  # type: ignore[arg-type]

        return __to_dict_with_complex_keys_from_others(self, keys, arg_tuples)  # type: ignore[arg-type]

    def dicts_to_instances(self, type_: TI) -> _DictOperation[TI]:
        return [type_(**element) for element in self]  # type: ignore[assignment]

    def group_by_key(self, key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, _DictOperation[T]]:  # type: ignore
        result: dict[Hashable, _DictOperation[T]] = {}

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        for element in self:
            group_key: Hashable = get_value_method(element, key, *args)

            if group_key in result:
                result[group_key].append(element)  # type: ignore[attr-defined]

            else:
                result[group_key] = list([element])  # type: ignore[attr-defined]

        return result

    def rename_keys(self, rename_keys: dict[Hashable, Hashable]) -> _DictOperation[T]:
        if not self:
            return _DictOperation()

        if not base.is_indexable(self):
            raise TypeError

        result: _DictOperation[T] = _DictOperation()

        for element in copy.deepcopy(self):
            for from_key, to_key in rename_keys.items():
                element[to_key] = element.pop(from_key)  # type: ignore[attr-defined]

            result.append(element)

        return result

    def map_for_keys(self, keys: list[Hashable], function: Callable[[Any], Any] | type, *args: Any) -> _DictOperation[dict[Any, Any]]:
        if not self:
            return _DictOperation()

        if not base.is_indexable(self):
            raise TypeError

        result: _DictOperation[T] = _DictOperation()

        for element in copy.deepcopy(self):
            for key in keys:
                element[key] = function(element[key], *args)  # type: ignore[attr-defined]

            result.append(element)

        return result
