from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Hashable
from typing import TypeVar

from typing_extensions import override
from typing_extensions import SupportsIndex  # type: ignore

from ext_list.dict_operations import _DictOperation  # type: ignore
from ext_list.list_operations import _ListOperation  # type: ignore
from ext_list.operator_operations import _OperatorOperation  # type: ignore

T = TypeVar('T')
TI = TypeVar('TI', bound=type)


class ExtList(_ListOperation[T], _OperatorOperation[T], _DictOperation[T]):
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
    def extract(self, key: Callable[[T, Any], Any] | property | str | Hashable, *args: Any) -> ExtList[Any]:
        """
        Extracts and returns a list of values associated with the given key from the objects.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to extract values for. If the key is function,
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

        Overrides :meth:`_ListOperation.extract`.
        """
        return super().extract(key, *args)  # type: ignore[assignment]

    @ override
    def extract_duplicates(self, other: ExtList[T]) -> ExtList[T]:  # type: ignore
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

        Overrides :meth:`_ListOperation.extract_duplicates`.
        """
        return super().extract_duplicates(other)  # type: ignore[assignment]

    @override
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

        Overrides :meth:`_ListOperation.is_duplicate`.
        """
        return super().is_duplicate()

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

        Overrides :meth:`_ListOperation.one`.
        """
        return super().one()

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

        Overrides :meth:`_ListOperation.first`.
        """
        return super().first()

    @override
    def map(self, function: Callable[[T, Any], Any] | type, *args: Any) -> ExtList[Any]:
        """
        Apply a function or constructor to each element.

        Args:
            function (Callable[[T, Any], Any] | type): The function or type to apply to each element.
            *args (Any): Additional arguments to pass to the function or type.

        Returns:
            ExtList[Any]: A new ExtList containing the mapped values.

        Examples:
            The following example demonstrates how to use the `map` method.

            >>> ext_list_1 = ExtList([1, 2, 3])
            >>> ext_list_1.map(float)
            [1.0, 2.0, 3.0]

        Overrides :meth:`_ListOperation.map`.
        """
        return super().map(function, *args)  # type: ignore[assignment]

    @override
    def equal(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that have the given key set to the given value.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.equal`.
        """
        return super().equal(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def not_equal(self, key: Callable[[T, Any], Any] | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that do not have the given key set to the given value.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.not_equal`.
        """
        return super().not_equal(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def greater(self, key: Callable[[T, Any], Any] | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Return a list of objects that are greater than the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[Callable[[T, Any], Any], property, Hashable]): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.greater`.
        """
        return super().greater(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def greater_or_equal(self, key: Callable[[T, Any], Any] | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Return a list of objects that are greater than or equal the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[Callable[[T, Any], Any], property, Hashable]): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.greater_or_equal`.
        """
        return super().greater_or_equal(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def less(self, key: Callable[[T, Any], Any] | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Return a list of objects that are less than the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[Callable[[T, Any], Any], property, Hashable]): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.less`.
        """
        return super().less(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def less_or_equal(self, key: Callable[[T, Any], Any] | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Return a list of objects that are less than or equal the specified compare_target, when the
        object is passed through the provided key function, property or hashable key.

        Args:
            key (Union[Callable[[T, Any], Any], property, Hashable]): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.less_or_equal`.
        """
        return super().less_or_equal(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def in_(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: list[Any], *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that have the given key set to one of the given values.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.in_`.
        """
        return super().in_(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def not_in_(self, key: Callable[[T, Any], Any] | property | str | Hashable, compare_target: list[Any], *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that do not have the given key set to any of the given values.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to compare values for. If the key is function,
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

        Overrides :meth:`_OperatorOperation.not_in_`.
        """
        return super().not_in_(key, compare_target, *args)  # type: ignore[assignment]

    @override
    def to_dict(self, key: Callable[[T, Any], Any] | property | str | Hashable, *args: Any) -> dict[Hashable, T]:
        """
        Converts the current object to a dictionary, using the given key as the dictionary key.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to use as the dictionary key. If the key is function,
                the callable will be executed and its result will be returned.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            dict[Hashable, T]: A dictionary of objects, using the given key as the dictionary key.

        Examples:
            The following example demonstrates how to use the `to_dict` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ext_list_1.to_dict('name')
            {'Alice': {'name': 'Alice', 'age': 25}, 'Bob': {'name': 'Bob', 'age': 30}}

            >>> ext_list_2 = ExtList([['Alice', 25], ['Bob', 30]])
            >>> ext_list_2.to_dict(0)
            {'Alice': ['Alice', 25], 'Bob': ['Bob', 30]}

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30)])
            >>> ext_list_3.to_dict(Person.name)
            {'Alice': Person('Alice', 25), 'Bob': Person('Bob', 30)}

            >>> ext_list_3.to_dict(Person.get_age_n_years_ago, 5)
            {20: Person('Alice', 25), 25: Person('Bob', 30)}

        Overrides :meth:`_DictOperation.to_dict`.
        """
        return super().to_dict(key, *args)  # type: ignore[assignment]

    @override
    def to_dict_list(self, keys: list[Callable[[T, Any], Any] | property | str | Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> ExtList[dict[str | Hashable, Any]]:
        """
        Converts the objects into a list of dictionaries, where each dictionary contains the specified keys
        and their corresponding values from the object.

        Args:
            keys (list[Callable[[T, Any], Any] | property | str | Hashable]): A list of keys to include in the dictionaries. Each key can
                be a function, property, string, or hashable object.
            arg_tuples (list[tuple[Any, ...]], optional): A list of argument tuples. Each tuple contains the arguments to be
                passed to the corresponding key function or property. Defaults to an empty list.

        Returns:
            ExtList[dict[str | Hashable, Any]]: A list of dictionaries, where each dictionary represents an element and contains
            the specified keys and their corresponding values.

        Examples:
            The following example demonstrates how to use the `to_dict_list` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ext_list_1.to_dict_list(['name'])
            [{'name': 'Alice'}, {'name': 'Bob'}]

            >>> ext_list_2 = ExtList([['Alice', 25], ['Bob', 30]])
            >>> ext_list_2.to_dict_list([0])
            [{0: 'Alice'}, {0: 'Bob'}]

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30)])
            >>> ext_list_3.to_dict_list([Person.name, Person.get_age_n_years_ago], [(), (5,)])
            [{'name': 'Alice', 'get_age_n_years_ago': 20}, {'name': 'Bob', 'get_age_n_years_ago': 25}]

        Overrides :meth:`_DictOperation.to_dict_list`.
        """
        return super().to_dict_list(keys, arg_tuples)  # type: ignore[assignment]

    @override
    def to_dict_with_complex_keys(self, keys: list[Callable[[T, Any], Any] | property | str] | list[Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> dict[tuple[Any, ...], T]:
        """
        Returns a dictionary of the objects in the `ExtList` with complex keys.

        Args:
            keys (List[Callable[[T, Any], Any] | property | str] | List[Hashable]): A list of the keys for the dictionary.
            arg_tuples (Tuple[Tuple[Any,...],...]): A list of tuples of the arguments. If key is a function, the arguments will be passed to the function.

        Returns:
            Dict[Tuple[Any, ...], T]: A dictionary of the objects in the `ExtList` with complex keys.

        Examples:
            The following example demonstrates how to use the `to_dict_with_complex_keys` method.

            >>> ext_list_1 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_1.to_dict_with_complex_keys([Person.name, Person.age])
            {('Alice', 25): Person('Alice', 25),
             ('Bob', 30): Person('Bob', 30),
             ('Charlie', 35): Person('Charlie', 35),
             ('David', 30): Person('David', 30)}

            >>> ext_list_1.to_dict_with_complex_keys(['name', Person.introduce, Person.get_age_n_years_ago], [(), (), (5,)])
            {('Alice', 'Alice is 25 years old.', 20): Person('Alice', 25),
             ('Bob', 'Bob is 30 years old.', 25): Person('Bob', 30),
             ('Charlie', 'Charlie is 35 years old.', 30): Person('Charlie', 35),
             ('David', 'David is 30 years old.', 25): Person('David', 30)}

        Overrides :meth:`_DictOperation.to_dict_with_complex_keys`.
        """
        return super().to_dict_with_complex_keys(keys, arg_tuples)

    @override
    def dicts_to_instances(self, type_: TI) -> ExtList[TI]:  # type: ignore[override]
        """
        Convert a list of dictionaries to a list of instances of the given class.

        Args:
            type_ (Type[TI]): The type of the instances to create.

        Returns:
            ExtList[TI]: A new ExtList containing the instances.

        Examples:
            The following example demonstrates how to use the `dicts_to_instances` method.

            >>> ext_list_1 = ExtList([{'name': 'alice', 'age': 25}, {'name': 'bob', 'age': 30}, {'name': 'charlie', 'age': 35}])
            >>> ext_list_1.dicts_to_instances(Person)
            [Person('alice', 25), Person('bob', 30), Person('charlie', 35)]

        Overrides :meth:`_DictOperation.dicts_to_instances`.
        """
        return super().dicts_to_instances(type_)  # type: ignore[assignment]

    @override
    def group_by_key(self, key: Callable[[T, Any], Any] | property | str | Hashable, *args: Any) -> dict[Hashable, ExtList[T]]:  # type: ignore[override]
        """Groups the objects of the list by a specified key.

        Args:
            key (Callable[[T, Any], Any] | property | str | Hashable): The key to group the objects by. This can be
                a function, property, string, or hashable object.
            *args (Any): Additional arguments to pass to the key function or property.

        Returns:
            dict[Hashable, ExtList[T]]: A dictionary of lists, where the keys are the result of applying the
            key function or property to the objects of the list, and the values are lists of objects
            with the same key.

        Examples:
            The following example demonstrates how to use the `dicts_to_instances` method.

            >>> ext_list_1 = ExtList([{'name': 'alice', 'age': 25}, {'name': 'bob', 'age': 30}, {'name': 'charlie', 'age': 35}, {'name': 'david', 'age': 30}])
            >>> ext_list_1.group_by_key('age')
            {25: [{'name': 'alice', 'age': 25}], 30: [{'name': 'bob', 'age': 30}, {'name': 'david', 'age': 30}], 35: [{'name': 'charlie', 'age': 35}]}

        Overrides :meth:`_DictOperation.group_by_key`.
        """
        return super().group_by_key(key, *args)  # type: ignore[assignment]

    @override
    def rename_keys(self, rename_keys: dict[Hashable, Hashable]) -> ExtList[T]:
        """
        Renames the keys in the objects based on the provided mapping dictionary.

        Args:
            rename_keys (dict[Hashable, Hashable]): A dictionary that maps the keys to be renamed. The keys in the dictionary
                represent the original keys, while the corresponding values represent the new keys.

        Returns:
            ExtList[T]: A list of objects with the renamed keys.

        Raises:
            TypeError: If the object is not indexable.

        Examples:
            >>> ext_list = ExtList([{'name': 'alice', 'age': 25}, {'name': 'bob', 'age': 30}])
            >>> ext_list.rename_keys({'name': 'Name', 'age': 'Age'})
            [{'Name': 'alice', 'Age': 25}, {'Name': 'bob', 'Age': 30}]

        Overrides :meth:`_DictOperation.rename_keys`.
        """
        return super().rename_keys(rename_keys)  # type: ignore[assignment]

    @override
    def map_for_keys(self, keys: list[Hashable], function: Callable[[Any], Any] | type, *args: Any) -> ExtList[dict[Any, Any]]:
        """
        Applies a function to specific keys of each element in the dictionary.

        Args:
            keys (list[Hashable]): A list of hashable keys to apply the function to.
            function (Callable[[Any], Any] | type): The function or type to apply to the keys.
                It should accept the value of each key as the first argument, followed by optional args.
            *args (Any): Optional arguments to be passed to the function along with each key's value.

        Returns:
            An instance of ExtList containing the modified dictionaries.

        Raises:
            TypeError: If the dictionary is not indexable.

        Example:
            The following example demonstrates how to use the `map_for_keys` method.

            >>> ext_list = ExtList([{'a': 1, 'b': 2, 'c': 3}])
            >>> keys = ['a', 'b']
            >>> function = lambda x, y: x + y
            >>> args = (10,)
            >>> ext_list.map_for_keys(keys, function, *args)
            {'a': 11, 'b': 12, 'c': 3}

        Overrides :meth:`_DictOperation.map_for_keys`.
        """
        return super().map_for_keys(keys, function, *args)  # type: ignore[assignment]
