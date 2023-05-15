from __future__ import annotations

from types import FunctionType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import List
from typing import TypeVar

from ext_list import base
T = TypeVar('T')


class OperatorOperation(List[T]):
    def equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Returns a list of objects that have the given key set to the given value.

        Args:
            key (FunctionType | property | str | Hashable): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_target (Any): The value to compare the objects' values to.
            *args (Any): If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList[T]: A list of objects that have the given key set to the given value. If no objects are found or the object
            is empty, an empty ExtList is returned.

        Examples:
            The following example demonstrates how to use the `equals` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.equals('age', 25)
            [{'name': 'Alice', 'age': 25}]

            >>> ext_list_2 = ExtList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ext_list_2.equals('graduated', None)
            [{'name': 'Alice', 'graduated': None}]

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_3.equals(Person.age, 30)
            [, Person('Bob', 30), Person('David', 30)]

            >>> ext_list_3.equals(Person.introduce, 'Alice is 25 years old.')
            [Person('Alice', 25)]

            >>> ext_list_3.equals(Person.get_age_n_years_ago, 20, 5)
            [Person('Alice', 25)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value is compare_target or value == compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def not_equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Returns a list of objects that do not have the given key set to the given value.

        Args:
            key (FunctionType | property | str | Hashable): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.

            compare_target (Any): The value to compare the objects' values to.

            *args (Any): If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList[T]: A list of objects that do not have the given key set to the given value.
            If no objects are found or the object is empty, an empty ExtList is returned.

        Examples:
            The following example demonstrates how to use the `not_equals` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.not_equals('age', 25)
            [{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}]

            >>> ext_list_2 = ExtList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ext_list_2.not_equals('graduated', None)
            [{'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}]

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_3.not_equals(Person.age, 30)
            [Person('Alice', 25), Person('Charlie', 35)]

            >>> ext_list_3.not_equals(Person.introduce, 'Alice is 25 years old.')
            [Person('Bob', 30), Person('Charlie', 35), Person('David', 30)]

            >>> ext_list_3.not_equals(Person.get_age_n_years_ago, 20, 5)
            [Person('Bob', 30), Person('Charlie', 35), Person('David', 30)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value is not compare_target and value != compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def greater(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Return a list of objects that are greater than the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[FunctionType, property, Hashable]): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_target (Any): The value to compare against.
            *args (Any): If key is a function, the arguments will be passed to the function.

        Returns:
            List[T]: A list of objects that are greater than the compare_target, when the
            object is passed through the provided key.

        Examples:
            The following example demonstrates how to use the `greater` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.greater('age', 30)
            [{'name': 'Charlie', 'age': 35}]

            >>> ext_list_2 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_2.greater(Person.age, 30)
            [Person('Charlie', 35)]

            >>> ext_list_2.greater(Person.get_age_n_years_ago, 25, 5)
            [Person('Charlie', 35)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value > compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def greater_or_equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Return a list of objects that are greater than or equal the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[FunctionType, property, Hashable]): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_target (Any): The value to compare against.
            *args (Any): Additional arguments to be passed to the key function.

        Returns:
            List[T]: A list of objects that are greater than or equal the compare_target, when the
            object is passed through the provided key.

        Examples:
            The following example demonstrates how to use the `greater_or_equal` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.greater_or_equal('age', 30)
            [{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}]

            >>> ext_list_2 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_2.greater_or_equal(Person.age, 30)
            [Person('Bob', 30), Person('Charlie', 35), Person('David', 30)]

            >>> ext_list_2.greater_or_equal(Person.get_age_n_years_ago, 25, 5)
            [Person('Bob', 30), Person('Charlie', 35), Person('David', 30)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value >= compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def less(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Return a list of objects that are less than the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[FunctionType, property, Hashable]): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_target (Any): The value to compare against.
            *args (Any): Additional arguments to be passed to the key function.

        Returns:
            List[T]: A list of objects that are less than the compare_target, when the
            object is passed through the provided key.

        Examples:
            The following example demonstrates how to use the `less` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.less('age', 30)
            [{'name': 'Alice', 'age': 25}]

            >>> ext_list_2 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_2.less(Person.age, 30)
            [Person('Alice', 25)]

            >>> ext_list_2.less(Person.get_age_n_years_ago, 25, 5)
            [Person('Alice', 25)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value < compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def less_or_equal(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Return a list of objects that are less than or equal the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[FunctionType, property, Hashable]): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_target (Any): The value to compare against.
            *args (Any): Additional arguments to be passed to the key function.

        Returns:
            List[T]: A list of objects that are less than or equal the compare_target, when the
            object is passed through the provided key.

        Examples:
            The following example demonstrates how to use the `less_or_equal` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.less_or_equal('age', 30)
            [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

            >>> ext_list_2 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_2.less_or_equal(Person.age, 30)
            [Person('Alice', 25), Person('Bob', 30), Person('David', 30)]

            >>> ext_list_2.less_or_equal(Person.get_age_n_years_ago, 25, 5)
            [Person('Alice', 25), Person('Bob', 30), Person('David', 30)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value <= compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def in_(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Returns a list of objects that have the given key set to one of the given values.

        Args:
            key (FunctionType | property | str | Hashable): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_targets (list): A list of values to compare the objects' values to.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList[T]: A list of objects that have the given key set to one of the given values. If no objects are found or
            the object is empty, an empty ExtList is returned.

        Examples:
            The following example demonstrates how to use the `in_` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.in_('age', [25, 30])
            [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

            >>> ext_list_2 = ExtList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ext_list_2.in_('graduated', [False, True])
            [{'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}]

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ext_list_3.in_(Person.age, [25, 35])
            [Person(Alice, 25), Person(Charlie, 35)]

            >>> ext_list_3.in_(Person.introduce, ['Alice is 25 years old.', 'Charlie is 35 years old.'])
            [Person('Alice', 25), Person('Charlie', 35)]

            >>> ext_list_3.in_(Person.get_age_n_years_ago, [20, 30], 5)
            [Person('Alice', 25), Person('Charlie', 35)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value in compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def not_in_(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> OperatorOperation[T]:
        """
        Returns a list of objects that do not have the given key set to any of the given values.

        Args:
            key (FunctionType | property | str | Hashable): The key to compare values for. If the key is function,
                the callable will be executed and its result will be returned.
            compare_targets (list): A list of values to compare the objects' values to.
            *args (Any): If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList[T]: A list of objects that do not have the given key set to any of the given values. If no objects are
            found or the object is empty, an empty ExtList is returned.

        Examples:
            The following example demonstrates how to use the `not_in_` method:

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.not_in_('age', [25, 30])
            [{'name': 'Charlie', 'age': 35}]

            >>> ext_list_2 = ExtList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ext_list_2.not_in_('graduated', [False, True])
            [{'name': 'Alice', 'graduated': None}]

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ext_list_3.not_in_(Person.age, [25, 35])
            [Person(Bob, 30)]

            >>> ext_list_3.not_in_(Person.introduce, ['Alice is 25 years old.', 'Charlie is 35 years old.'])
            [Person('Bob', 30)]

            >>> ext_list_3.not_in_(Person.get_age_n_years_ago, [20, 30], 5)
            [Person('Bob', 30)]
        """
        def __operator(value: Any, compare_target: Any) -> bool:
            return value not in compare_target

        return self.__operator_base(key, compare_target, __operator, *args)

    def __operator_base(self, key: FunctionType | property | str | Hashable, compare_target: Any, operator: Callable[[Any, Any], bool], *args: Any) -> OperatorOperation[T]:
        if not self:
            return OperatorOperation()

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        return OperatorOperation([element for element in self if operator(get_value_method(element, key, *args), compare_target)])
