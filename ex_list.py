from __future__ import annotations

import copy
from typing import Any
from typing import Hashable
from typing import Iterable
from typing import SupportsIndex
from typing import TypeVar

from typing_extensions import override

T = TypeVar('T')


class ExList(list[T]):
    def __init__(self, iterable: list[T] = []) -> None:
        ExList.__is_all_elements_single_type(iterable)
        super().__init__(iterable)

    @ staticmethod
    def __is_all_elements_single_type(iterable: list[Any]) -> None:
        if not iterable:
            return

        allowed_type: Any = type(iterable[0])

        if not all(isinstance(element, allowed_type) for element in iterable):
            raise TypeError(
                'Expected all elements to be of the same type.',
            )

    @override
    def __add__(self, other: ExList[T]) -> ExList[T]:  # type: ignore[override]
        if not self:
            return other

        if not other:
            return self

        if not isinstance(self[0], type(other[0])):
            raise TypeError(
                f'Expected ExList[{type(self[0])}] but got ExList[{type(other[0])}].',
            )

        return ExList(super().__add__(other))

    @override
    def __iadd__(self, other: ExList[T]) -> ExList[T]:  # type: ignore[override]
        if not self:
            super().__iadd__(other)

            return other

        if not other:
            super().__iadd__(other)

            return self

        if not isinstance(self[0], type(other[0])):
            raise TypeError(
                f'Expected ExList[{type(self[0])}] but got ExList[{type(other[0])}].',
            )

        super().__iadd__(other)

        return self

    @ override
    def append(self, element: T) -> None:
        if not self:
            super().append(element)
            return

        if not isinstance(element, type(self[0])):
            raise TypeError(
                f'Expected {type(self[0])} but got {type(element)}.',
            )

        super().append(element)

    @ override
    def extend(self, iterable: Iterable[T]) -> None:
        if not self:
            super().extend(iterable)
            return

        if not iterable:
            return

        if not isinstance(self[0], type(iterable[0])):  # type: ignore[index]
            raise TypeError(
                f'Expected ExList[{type(self[0])}] but got ExList[{type(iterable[0])}].',  # type: ignore[index]
            )

        super().extend(iterable)

    @ override
    def insert(self, index: SupportsIndex, element: T) -> None:
        if not self:
            super().insert(index, element)
            return

        if not isinstance(element, type(self[0])):
            raise TypeError(
                f'Expected {type(self[0])} but got {type(element)}.',
            )

        super().insert(index, element)

    def extract(self, key: Hashable, execute_callable: bool = False) -> ExList[Any]:
        if not self:
            return ExList()

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__extract_from_dict_or_list(key, execute_callable)

        if isinstance(key, str):
            return self.__extract_from_others(key, execute_callable)

        raise TypeError

    def __extract_from_dict_or_list(self, key: Hashable, execute_callable: bool) -> ExList[Any]:
        if execute_callable:
            return ExList([element[key]() for element in self])  # type: ignore
        else:
            return ExList([element[key] for element in self])  # type: ignore[index]

    def __extract_from_others(self, key: str, execute_callable: bool) -> ExList[Any]:
        if execute_callable:
            return ExList([getattr(element, key)() for element in self])

        return ExList([getattr(element, key) for element in self])

    def equals(self, key: Hashable, compare_target: Any) -> ExList[T]:
        if not self:
            return ExList()

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__equals_from_dict_or_list(key, compare_target)

        if isinstance(key, str):
            return self.__equals_from_others(key, compare_target)

        raise TypeError

    def __equals_from_dict_or_list(self, key: Hashable, compare_target: Any) -> ExList[T]:
        if compare_target in {None, True, False}:
            return ExList([element for element in self if element[key] is compare_target])  # type: ignore[index]

        return ExList([element for element in self if element[key] == compare_target])  # type: ignore[index]

    def __equals_from_others(self, key: str, compare_target: Any) -> ExList[T]:
        if compare_target in {None, True, False}:
            return ExList([element for element in self if getattr(element, key) is compare_target])

        return ExList([element for element in self if getattr(element, key) == compare_target])

    def not_equals(self, key: Hashable, compare_target: Any) -> ExList[T]:
        if not self:
            return ExList()

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__not_equals_from_dict_or_list(key, compare_target)

        if isinstance(key, str):
            return self.__not_equals_from_others(key, compare_target)

        raise TypeError

    def __not_equals_from_dict_or_list(self, key: Hashable, compare_target: Any) -> ExList[T]:
        if compare_target in {None, True, False}:
            return ExList([element for element in self if element[key] is not compare_target])  # type: ignore[index]

        return ExList([element for element in self if element[key] != compare_target])  # type: ignore[index]

    def __not_equals_from_others(self, key: str, compare_target: Any) -> ExList[T]:
        if compare_target in {None, True, False}:
            return ExList([element for element in self if getattr(element, key) is not compare_target])

        return ExList([element for element in self if getattr(element, key) != compare_target])

    def in_(self, key: Hashable, compare_targets: list[Any]) -> ExList[T]:
        if not self:
            return ExList()

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__in_from_dict_or_list(key, compare_targets)

        if isinstance(key, str):
            return self.__in_from_others(key, compare_targets)

        raise TypeError

    def __in_from_dict_or_list(self, key: Hashable, compare_targets: list[Any]) -> ExList[T]:
        return ExList([element for element in self if element[key] in compare_targets])  # type: ignore[index]

    def __in_from_others(self, key: str, compare_targets: list[Any]) -> ExList[T]:
        return ExList([element for element in self if getattr(element, key) in compare_targets])

    def not_in_(self, key: Hashable | str, compare_targets: list[Any]) -> ExList[T]:
        if not self:
            return ExList()

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__not_in_from_dict_or_list(key, compare_targets)

        if isinstance(key, str):
            return self.__not_in_from_others(key, compare_targets)

        raise TypeError

    def __not_in_from_dict_or_list(self, key: Hashable, compare_targets: list[Any]) -> ExList[T]:
        return ExList([element for element in self if element[key] not in compare_targets])  # type: ignore[index]

    def __not_in_from_others(self, key: str, compare_targets: list[Any]) -> ExList[T]:
        return ExList([element for element in self if getattr(element, key) not in compare_targets])

    def extract_duplicates(self, compare_ex_list: ExList[T]) -> ExList[T]:
        return ExList([element for element in self if element in compare_ex_list])

    def is_duplicate(self) -> bool:
        if not self:
            return False

        tmp_ex_list: ExList[T] = copy.deepcopy(self)

        for _ in range(len(tmp_ex_list)):
            if tmp_ex_list.pop() in tmp_ex_list:
                return True

        return False

    def one(self) -> T | None:
        try:
            return self[0]
        except IndexError:
            return None

    def first(self) -> T:
        return self[0]

    def to_dict(self, key: Hashable) -> dict[Hashable, T]:
        if not self:
            return {}

        if isinstance(self[0], dict):
            return self.__to_dict_from_dict(key)

        if isinstance(key, str):
            return self.__to_dict_from_others(key)

        raise TypeError

    def __to_dict_from_dict(self, key: Hashable) -> dict[Hashable, T]:
        return {element[key]: element for element in self}  # type: ignore[index]

    def __to_dict_from_others(self, key: str) -> dict[Hashable, T]:
        return {getattr(element, key): element for element in self}

    def to_dict_with_complex_keys(self, keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        if not self:
            return {}

        if isinstance(self[0], dict):
            return self.__to_dict_with_complex_keys_from_dict(keys)

        if all([isinstance(key, str) for key in keys]):
            return self.__to_dict_with_complex_keys_from_others(keys)  # type: ignore[arg-type]

        raise TypeError

    def __to_dict_with_complex_keys_from_dict(self, keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        return {tuple(element[key] for key in keys): element for element in self}  # type: ignore[index]

    def __to_dict_with_complex_keys_from_others(self, keys: list[str]) -> dict[tuple[Any, ...], T]:
        return {tuple(getattr(element, key) for key in keys): element for element in self}
