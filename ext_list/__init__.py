from __future__ import annotations

from types import FunctionType
from typing import Any
from typing import Hashable
from typing import SupportsIndex
from typing import TypeVar

from typing_extensions import override

from ext_list.dict_operations import DictOperation
from ext_list.list_operations import ListOperation
from ext_list.operator_operations import OperatorOperation

T = TypeVar('T')
TI = TypeVar('TI', bound=type)


class ExtList(ListOperation[T], OperatorOperation[T], DictOperation[T]):
    """
    Note:
        The following class is used to describe each method of ExtList:

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.__name = name
            ...         self.__age = age
            ...
            ...     def introduce(self):
            ...         return f'{self.name} is {self.age} years old.'
            ...
            ...     def get_age_n_years_ago(self, n: int) -> int:
            ...        return self.age - n
            ...
            ...     @property
            ...     def name(self):
            ...         return self.__name
            ...
            ...     @property
            ...     def age(self):
            ...         return self.__age
            ...
            ...     def __repr__(self):
            ...         return f'Person(\'{self.name}\', {self.age})'
    """

    def __init__(self, iterable: list[T] = []) -> None:
        super().__init__(iterable)

    @staticmethod
    def __validate_ext_list(iterable: Any) -> None:
        if not isinstance(iterable, ExtList):
            raise TypeError(f'Expected <class \'ExtList\'> but got {type(iterable)}')

    @ override
    def __add__(self, other: ExtList[T]) -> ExtList[T]:  # type: ignore[override]
        self.__validate_ext_list(other)

        if not self:
            return other

        if not other:
            return self

        return ExtList(super().__add__(other))

    @ override
    def __iadd__(self, other: ExtList[T]) -> ExtList[T]:  # type: ignore[override]
        self.__validate_ext_list(other)

        if not self:
            super().__iadd__(other)
            return other

        if not other:
            super().__iadd__(other)
            return self

        super().__iadd__(other)

        return self

    @ override
    def append(self, element: T) -> None:
        if not self:
            super().append(element)
            return

        super().append(element)

    @ override
    def extend(self, other: ExtList[T]) -> None:  # type: ignore[override]
        if not isinstance(other, ExtList):  # type: ignore
            raise TypeError(f'Expected ExtList but got {type(other)}')

        if not self:
            super().extend(other)
            return

        if not other:
            return

        super().extend(other)

    @ override
    def insert(self, index: SupportsIndex, element: T) -> None:
        if not self:
            super().insert(index, element)
            return

        super().insert(index, element)

    @ override
    def extract(self, key: FunctionType | property | str | Hashable, *args: Any) -> ExtList[Any]:
        return self.__class__(super().extract(key, *args))

    @ override
    def extract_duplicates(self, other: ExtList[T]) -> ExtList[T]:  # type: ignore
        return self.__class__(super().extract_duplicates(other))

    @override
    def map(self, function: FunctionType | type, *args: Any) -> ExtList[Any]:
        return self.__class__(super().map(function, *args))

    @override
    def equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        return self.__class__(super().equal(key, compare_target, *args))

    @override
    def not_equal(self, key: FunctionType | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        return self.__class__(super().not_equal(key, compare_target, *args))

    @override
    def greater(self, key: FunctionType | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        return self.__class__(super().greater(key, compare_target, *args))

    @override
    def greater_or_equal(self, key: FunctionType | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        return self.__class__(super().greater_or_equal(key, compare_target, *args))

    @override
    def less(self, key: FunctionType | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        return self.__class__(super().less(key, compare_target, *args))

    @override
    def less_or_equal(self, key: FunctionType | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        return self.__class__(super().less_or_equal(key, compare_target, *args))

    @override
    def in_(self, key: FunctionType | property | str | Hashable, compare_target: list[Any], *args: Any) -> ExtList[T]:
        return self.__class__(super().in_(key, compare_target, *args))

    @override
    def not_in_(self, key: FunctionType | property | str | Hashable, compare_target: list[Any], *args: Any) -> ExtList[T]:
        return self.__class__(super().not_in_(key, compare_target, *args))

    @override
    def to_dict_list(self, keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> ExtList[dict[str | Hashable, Any]]:
        return self.__class__(super().to_dict_list(keys, arg_tuples))

    @override
    def dicts_to_instances(self, type_: TI) -> ExtList[TI]:  # type: ignore[override]
        return self.__class__(super().dicts_to_instances(type_))

    @override
    def group_by_key(self, key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, ExtList[T]]:  # type: ignore[override]
        return super().group_by_key(key, *args)  # type: ignore[assignment]

    @override
    def rename_keys(self, rename_keys: dict[Hashable, Hashable]) -> ExtList[T]:
        return self.__class__(super().rename_keys(rename_keys))
