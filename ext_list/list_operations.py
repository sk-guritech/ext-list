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


class ListOperation(List[T]):
    def extract(self, key: FunctionType | property | str | Hashable, *args: Any) -> ListOperation[Any]:
        """
        Extracts and returns a list of values associated with the given key from the objects.

        Args:
            key (FunctionType | property | str | Hashable): The key to extract values for. If the key is function,
                the callable will be executed and its result will be returned.
            *args (Any): If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList[Any]: A list of values associated with the given key.

        Examples:
            The following example demonstrates how to use the 'extract' method.

            >>> ext_list_1 = ExtList([{'a': 1}, {'a': 2}, {'a': 3}])
            >>> ext_list_1.extract('a')
            [1, 2, 3]

            >>> ext_list_2 = ExtList([[1, 2], [3, 4], [5, 6]])
            >>> ext_list_2.extract(0)
            [1, 3, 5]

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ext_list_3.extract(Person.name)
            ['Alice', 'Bob', 'Charlie']

            >>> ext_list_3.extract(Person.introduce)
            ['Alice is 25 years old.', 'Bob is 30 years old.', 'Charlie is 35 years old.']

            >>> ext_list_3.extract(Person.get_age_n_years_ago, 5)
            [20, 25, 30]
        """
        if not self:
            return ListOperation([])

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        return ListOperation([get_value_method(element, key, *args) for element in self])

    def extract_duplicates(self, other: ListOperation[T]) -> ListOperation[T]:
        """
        Returns a list of objects that are in both the current object and the given object.

        Args:
            compare_ext_list (ExtList[T]): The object to compare the current object to.

        Returns:
            ExtList[T]: A list of objects that are in both the current object and the given object. If no objects are found
            or the object is empty, an empty ExtList is returned.

        Examples:
            The following example demonstrates how to use the `extract_duplicates` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ext_list_2 = ExtList([{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.extract_duplicates(ext_list_2)
            [{'name': 'Bob', 'age': 30}]
        """
        return self.__class__([element for element in self if element in other])

    def is_duplicate(self) -> bool:
        """
        Returns `True` if there are any duplicates in the current object, `False` otherwise.

        Returns:
            bool: `True` if there are any duplicates in the current object, `False` otherwise.

        Examples:
            The following example demonstrates how to use the `is_duplicate` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Alice', 'age': 25}])
            >>> ext_list_1.is_duplicate()
            True

            >>> ext_list_2 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_2.is_duplicate()
            False
        """
        if not self:
            return False

        tmp_ext_list: list[T] = copy.deepcopy(self)

        for _ in range(len(tmp_ext_list)):
            if tmp_ext_list.pop() in tmp_ext_list:
                return True

        return False

    def one(self) -> T | None:
        """
        Returns the first object in the current object. If the object is empty, `None` is returned.

        Returns:
            T or None: The first object in the current object, or `None` if the object is empty.

        Examples:
            The following example demonstrates how to use the `one` method to return the first object in an ExtList:

            >>> ext_list_1 = ExtList([1, 2, 3])
            >>> ext_list_1.one()
            1

            The following example demonstrates how to use the `one` method to return `None` when the object is empty:

            >>> ext_list_2 = ExtList([])
            >>> ext_list_2.one()
            None
        """
        try:
            return self[0]

        except IndexError:
            return None

    def first(self) -> T:
        """
        Returns the first object in the current object.

        Returns:
            T: The first object in the current object.

        Raises:
            IndexError: If the object is empty.

        Examples:
            The following example demonstrates how to use the `first` method to return the first object in an ExtList:

            >>> ext_list_1 = ExtList([1, 2, 3])
            >>> ext_list_1.first()
            1
        """
        return self[0]

    def map(self, function: FunctionType | type, *args: Any) -> ListOperation[Any]:
        """
        Apply a function or constructor to each element.

        Args:
            function (FunctionType | type): The function or type to apply to each element.
            *args (Any): Additional arguments to pass to the function or type.

        Returns:
            ExtList[Any]: A new ExtList containing the mapped values.

        Examples:
            The following example demonstrates how to use the `map` method.

            >>> ext_list_1 = ExtList([1, 2, 3])
            >>> ext_list_1.map(float)
            [1.0, 2.0, 3.0]
        """
        return self.__class__([function(element, *args) for element in self])
