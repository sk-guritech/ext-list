from __future__ import annotations

import copy
from types import FunctionType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import List
from typing import TypeVar

from ext_list import base
T = TypeVar('T')


class _ListOperation(List[T]):
    def extract(self, key: FunctionType | property | str | Hashable, *args: Any) -> _ListOperation[Any]:
        if not self:
            return _ListOperation([])

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        return _ListOperation([get_value_method(element, key, *args) for element in self])

    def extract_duplicates(self, other: _ListOperation[T]) -> _ListOperation[T]:
        return self.__class__([element for element in self if element in other])

    def is_duplicate(self) -> bool:
        if not self:
            return False

        tmp_ext_list: list[T] = copy.deepcopy(self)

        for _ in range(len(tmp_ext_list)):
            if tmp_ext_list.pop() in tmp_ext_list:
                return True

        return False

    def one(self) -> T | None:
        try:
            return self[0]

        except IndexError:
            return None

    def first(self) -> T:
        return self[0]

    def map(self, function: FunctionType | type, *args: Any) -> _ListOperation[Any]:
        return self.__class__([function(element, *args) for element in self])
