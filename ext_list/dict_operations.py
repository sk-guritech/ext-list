from __future__ import annotations

import copy
from types import FunctionType
from types import GetSetDescriptorType
from types import MethodDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterable
from typing import List
from typing import TypeVar

from ext_list import base

T = TypeVar('T')
TI = TypeVar('TI')


class _DictOperation(List[T]):  # type: ignore
    def to_dict(self, key: Callable[[T, Any], Any] | property | str | Hashable, *args: Any) -> dict[Hashable, T]:
        if not self:
            return {}

        if base.is_indexable(self):
            return {element[key]: element for element in self if element[key]}  # type: ignore[attr-defined]

        if isinstance(key, str):
            key = getattr(type(self[0]), key)

        if callable(key):
            return {key(element, *args): element for element in self}

        if isinstance(key, property) or isinstance(key, GetSetDescriptorType):
            return {key.__get__(element): element for element in self}

        raise KeyError

    def to_dict_list(self, keys: list[Callable[[T, Any], Any] | property | str | Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> Iterable[dict[str | Hashable, T]]:
        def __to_dict_list_from_indexable_object(elements: list[T], keys: list[Hashable]) -> list[dict[str | Hashable, T]]:
            return [{key: element[key] for key in keys} for element in elements]   # type: ignore[attr-defined]

        def __to_dict_list_from_others(
            elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]],
        ) -> list[dict[str | Hashable, T]]:
            if not arg_tuples:
                arg_tuples = list(tuple() for _ in range(len(keys)))

            result: list[dict[str | Hashable, T]] = []

            for element in elements:
                row: dict[str | Hashable, T] = __generate_dict_from_specified_keys(elements, keys, arg_tuples, element)

                result.append(row)

            return result

        def __generate_dict_from_specified_keys(
            elements: list[T], keys: list[Callable[[T, Any], Any] | property | str | Hashable], arg_tuples: list[tuple[Any, ...]], element: T,
        ) -> dict[str | Hashable, Any]:
            result: dict[str | Hashable, Any] = {}

            for arg_tuple, key in zip(arg_tuples, keys):
                if isinstance(key, property):
                    dict_key: str | Hashable = key.fget.__name__  # type: ignore[attr-defined]

                elif isinstance(key, FunctionType) or isinstance(key, MethodDescriptorType) or isinstance(key, GetSetDescriptorType):
                    dict_key = key.__name__

                elif isinstance(key, str):
                    dict_key = key

                else:
                    dict_key = key

                get_value_method = base.determine_get_value_method(elements, key)
                result[dict_key] = get_value_method(element, key, *arg_tuple)  # type: ignore[assignment]

            return result

        if not self:
            return self.__class__()

        if base.is_indexable(self):
            return self.__class__(__to_dict_list_from_indexable_object(self, keys))  # type: ignore[assignment]

        return self.__class__(__to_dict_list_from_others(self, keys, arg_tuples))  # type: ignore[assignment]

    def to_dict_with_complex_keys(self, keys: list[Callable[[T, Any], Any] | property | str] | list[Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> dict[tuple[Any, ...], T]:
        def __to_dict_with_complex_keys_from_indexable_object(elements: list[T], keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
            return {tuple(element[key] for key in keys): element for element in elements}  # type: ignore[index]

        def __to_dict_with_complex_keys_from_others(
            elements: list[T], keys: list[Callable[[T, Any], Any] | property | str], arg_tuples: list[tuple[Any, ...]],
        ) -> dict[tuple[Any, ...], T]:
            result: dict[tuple[Any, ...], T] = {}

            if not arg_tuples:
                arg_tuples = list(tuple() for _ in range(len(keys)))

            for element in elements:
                tupled_key: tuple[Any, ...] = __generate_tupled_key(elements, keys, element, arg_tuples)
                result[tupled_key] = element

            return result

        def __generate_tupled_key(elements: list[T], keys: list[Callable[[T, Any], Any] | property | str], element: T, arg_tuples: list[tuple[Any, ...]]) -> tuple[Any, ...]:
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

    def dicts_to_instances(self, type_: TI) -> Iterable[TI]:
        return self.__class__([type_(**element) for element in self])  # type: ignore[assignment]

    def group_by_key(self, key: Callable[[T, Any], Any] | property | str | Hashable, *args: Any) -> dict[Hashable, Iterable[T]]:  # type: ignore
        result: dict[Hashable, Iterable[T]] = {}

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        for element in self:
            group_key: Hashable = get_value_method(element, key, *args)

            if group_key in result:
                result[group_key].append(element)  # type: ignore[attr-defined]

            else:
                result[group_key] = list([element])  # type: ignore[attr-defined]

        return result

    def rename_keys(self, rename_keys: dict[Hashable, Hashable]) -> Iterable[T]:
        def __copy_object() -> Iterable[Any]:
            if isinstance(self[0], dict):
                return [dict(element) for element in self]  # type: ignore[assignment]

            elif isinstance(self[0], list):
                return [list(element) for element in self]  # type: ignore[assignment]

            else:
                return copy.deepcopy(list(self))

        def __swap_keys(element: T, rename_keys: dict[Hashable, Hashable]):
            for from_key, to_key in rename_keys.items():
                element[to_key] = element[from_key]  # type: ignore[attr-defined]
                del element[from_key]  # type: ignore[assignment]

            return element

        if not self:
            return self.__class__()

        if not base.is_indexable(self):
            raise TypeError

        copied_elements = __copy_object()

        return self.__class__([__swap_keys(element, rename_keys) for element in copied_elements])

    def map_for_keys(self, keys: list[Hashable], function: Callable[[Any], Any] | type, *args: Any) -> Iterable[dict[Any, Any]]:
        def __copy_object() -> Iterable[Any]:
            if isinstance(self[0], dict):
                return [dict(element) for element in self]  # type: ignore[assignment]

            elif isinstance(self[0], list):
                return [list(element) for element in self]  # type: ignore[assignment]

            else:
                return copy.deepcopy(list(self))

        if not self:
            return self.__class__()

        if not base.is_indexable(self):
            raise TypeError

        result: Iterable[dict[Any, Any]] = self.__class__()

        for element in __copy_object():
            for key in keys:
                element[key] = function(element[key], *args)  # type: ignore[attr-defined]

            result.append(element)  # type: ignore[assignment]

        return result
