from __future__ import annotations

from types import FunctionType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import List
from typing import TypeVar

from ext_list import base
T = TypeVar('T')


class _OperatorOperation(List[T]):
    def equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value is compare_target or value == compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def not_equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value is not compare_target and value != compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def greater(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value > compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def greater_or_equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value >= compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def less(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value < compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def less_or_equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value <= compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def in_(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value in compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def not_in_(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> _OperatorOperation[T]:
        def __operator(value: Any, compare_target: Any) -> bool:
            return value not in compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def __operator_base(self, key: FunctionType | property | str | Hashable, compare_target: Any, operator: Callable[[Any, Any], bool], *args: Any) -> _OperatorOperation[T]:
        if not self:
            return _OperatorOperation()

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        return _OperatorOperation([element for element in self if operator(get_value_method(element, key, *args), compare_target)])
