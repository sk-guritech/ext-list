from __future__ import annotations

import copy
from types import FunctionType
from typing import Any
from typing import Hashable
from typing import SupportsIndex
from typing import TypeVar

from typing_extensions import override

T = TypeVar('T')


class ExList(list[T]):
    """
    Note:
        The following class is used to describe each method of ExList:

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.__name = name
            ...         self.__age = age
            ...
            ...     def introduce(self):
            ...         return f'{self.name} is {self.age} years old.'
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
        ExList.__validate_all_elements_are_single_type(iterable)
        super().__init__(iterable)

    @staticmethod
    def __validate_all_elements_are_single_type(iterable: list[Any]) -> None:
        if not iterable:
            return

        allowed_type: Any = type(iterable[0])

        if not all(isinstance(element, allowed_type) for element in iterable):
            raise TypeError(
                'Expected all elements to be of the same type.',
            )

    def __validate_same_type(self, element: T) -> None:
        if not isinstance(element, type(self[0])):
            raise TypeError(
                f'Expected {type(self[0])} but got {type(element)}.',
            )

    def __validate_same_type_ex_list(self, other: ExList[T]):
        if not isinstance(self[0], type(other[0])):  # type: ignore[index]
            raise TypeError(
                f'Expected ExList[{type(self[0])}] but got ExList[{type(other[0])}].',  # type: ignore[index]
            )

    def __is_indexable(self) -> bool:
        return hasattr(self[0], '__getitem__')

    @override
    def __add__(self, other: ExList[T]) -> ExList[T]:  # type: ignore[override]
        if not self:
            return other

        if not other:
            return self

        self.__validate_same_type_ex_list(other)

        return ExList(super().__add__(other))

    @override
    def __iadd__(self, other: ExList[T]) -> ExList[T]:  # type: ignore[override]
        if not self:
            super().__iadd__(other)

            return other

        if not other:
            super().__iadd__(other)

            return self

        self.__validate_same_type_ex_list(other)

        super().__iadd__(other)

        return self

    @ override
    def append(self, element: T) -> None:
        if not self:
            super().append(element)

            return

        self.__validate_same_type(element)

        super().append(element)

    @ override
    def extend(self, other: ExList[T]) -> None:  # type: ignore[override]
        if not self:
            super().extend(other)

            return

        if not other:
            return

        self.__validate_same_type_ex_list(other)

        super().extend(other)

    @ override
    def insert(self, index: SupportsIndex, element: T) -> None:
        if not self:
            super().insert(index, element)
            return

        self.__validate_same_type(element)

        super().insert(index, element)

    def extract(self, key: FunctionType | property | Hashable) -> ExList[Any]:
        """
        Extracts and returns a list of values associated with the given key from the objects.

        Args:
            key (FunctionType | property | Hashable): The key to extract values for. If the key is function,
                the callable will be executed and its result will be returned.

        Returns:
            ExList: A list of values associated with the given key. If no values are found or the object
                is empty, an empty ExList is returned.

        Examples:
            The following example demonstrates how to use the 'extract' method.

            >>> ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
            >>> ex_list_1.extract('a')
            [1, 2, 3]

            >>> ex_list_2 = ExList([[1, 2], [3, 4], [5, 6]])
            >>> ex_list_2.extract(0)
            [1, 3, 5]

            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.extract(Person.name)
            ['Alice', 'Bob', 'Charlie']

            >>> ex_list_3.extract(Person.introduce)
            ['Alice is 25 years old.', 'Bob is 30 years old.', 'Charlie is 35 years old.']
        """
        if not self:
            return ExList()

        if self.__is_indexable():
            return ExList([element[key] for element in self])  # type: ignore[index]

        if isinstance(key, FunctionType):
            return ExList([key(element) for element in self])

        return ExList([key.fget(element) for element in self])  # type: ignore[attr-defined]

    def equals(self, key: FunctionType | property | Hashable, compare_target: Any) -> ExList[T]:
        """
        Returns a list of objects that have the given key set to the given value.

        Args:
            key (FunctionType | property | Hashable): The key to search for.
            compare_target (Any): The value to compare the objects' values to.

        Returns:
            ExList: A list of objects that have the given key set to the given value. If no objects are found or the object
                is empty, an empty ExList is returned.

        Examples:
            The following example demonstrates how to use the `equals` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.equals('age', 25)
            [{'name': 'Alice', 'age': 25}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.equals('graduated', None)
            [{'name': 'Alice', 'graduated': None}]

            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ex_list_3.equals(Person.age, 30)
            [, Person('Bob', 30), Person('David', 30)]

            >>> ex_list_3.equals(Person.introduce, 'Alice is 25 years old.')
            [Person('Alice', 25)]
        """
        if not self:
            return ExList()

        if self.__is_indexable():
            return self.__equals_from_indexable_object(key, compare_target)

        if isinstance(key, FunctionType):
            if compare_target in {None, False, True}:
                return ExList([element for element in self if key(element) is compare_target])

            return ExList([element for element in self if key(element) == compare_target])

        if compare_target in {None, False, True}:
            return ExList([element for element in self if key.fget(element) is compare_target])  # type: ignore[attr-defined]

        return ExList([element for element in self if key.fget(element) == compare_target])  # type: ignore[attr-defined]

    def __equals_from_indexable_object(self, key: Hashable, compare_target: Any) -> ExList[T]:
        if compare_target in {None, True, False}:
            return ExList([element for element in self if element[key] is compare_target])  # type: ignore[index]

        return ExList([element for element in self if element[key] == compare_target])  # type: ignore[index]

    def not_equals(self, key: FunctionType | property | Hashable, compare_target: Any) -> ExList[T]:
        """
        Returns a list of objects that do not have the given key set to the given value.

        Args:
            key (FunctionType | property | Hashable): The key to search for.
            compare_target (Any): The value to compare the objects' values to.

        Returns:
            ExList: A list of objects that do not have the given key set to the given value. If no objects are found or the
                object is empty, an empty ExList is returned.

        Examples:
            The following example demonstrates how to use the `not_equals` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.not_equals('age', 25)
            [{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.not_equals('graduated', None)
            [{'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}]

            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ex_list_3.not_equals(Person.age, 30)
            [Person('Alice', 25), Person('Charlie', 35)]

            >>> ex_list_3.not_equals(Person.introduce, 'Alice is 25 years old.')
            [Person('Bob', 30), Person('Charlie', 35), Person('David', 30)]
        """
        if not self:
            return ExList()

        if self.__is_indexable():
            return self.__not_equals_from_indexable_object(key, compare_target)

        if isinstance(key, FunctionType):
            if compare_target in {None, False, True}:
                return ExList([element for element in self if key(element) is not compare_target])

            return ExList([element for element in self if key(element) != compare_target])

        if compare_target in {None, False, True}:
            return ExList([element for element in self if key.fget(element) is not compare_target])  # type: ignore[attr-defined]

        return ExList([element for element in self if key.fget(element) != compare_target])  # type: ignore[attr-defined]

    def __not_equals_from_indexable_object(self, key: Hashable, compare_target: Any) -> ExList[T]:
        if compare_target in {None, True, False}:
            return ExList([element for element in self if element[key] is not compare_target])  # type: ignore[index]

        return ExList([element for element in self if element[key] != compare_target])  # type: ignore[index]

    def in_(self, key: FunctionType | property | Hashable, compare_targets: list[Any]) -> ExList[T]:
        """
        Returns a list of objects that have the given key set to one of the given values.

        Args:
            key (FunctionType | property | Hashable): The key to search for.
            compare_targets (list): A list of values to compare the objects' values to.

        Returns:
            ExList: A list of objects that have the given key set to one of the given values. If no objects are found or
                the object is empty, an empty ExList is returned.

        Examples:
            The following example demonstrates how to use the `in_` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.in_('age', [25, 30])
            [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.in_('graduated', [False, True])
            [{'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}]

            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.in_(Person.age, [25, 35])
            [Person(Alice, 25), Person(Charlie, 35)]

            >>> ex_list_3.in_(Person.introduce, ['Alice is 25 years old.', 'Charlie is 35 years old.'])
            [Person('Alice', 25), Person('Charlie', 35)]
        """
        if not self:
            return ExList()

        if self.__is_indexable():
            return ExList([element for element in self if element[key] in compare_targets])  # type: ignore[index]

        if isinstance(key, FunctionType):
            return ExList([element for element in self if key(element) in compare_targets])

        return ExList([element for element in self if key.fget(element) in compare_targets])  # type: ignore[attr-defined]

    def not_in_(self, key: FunctionType | property | Hashable, compare_targets: list[Any]) -> ExList[T]:
        """
        Returns a list of objects that do not have the given key set to any of the given values.

        Args:
            key (Hashable or str): The key to search for.
            compare_targets (list): A list of values to compare the objects' values to.

        Returns:
            ExList: A list of objects that do not have the given key set to any of the given values. If no objects are
                found or the object is empty, an empty ExList is returned.

        Examples:
            The following example demonstrates how to use the `not_in_` method:

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.not_in_('age', [25, 30])
            [{'name': 'Charlie', 'age': 35}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.not_in_('graduated', [False, True])
            [{'name': 'Alice', 'graduated': None}]

            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.not_in_(Person.age, [25, 35])
            [Person(Bob, 30)]

            >>> ex_list_3.not_in_(Person.introduce, ['Alice is 25 years old.', 'Charlie is 35 years old.'])
            [Person('Bob', 30)]
        """
        if not self:
            return ExList()

        if self.__is_indexable():
            return ExList([element for element in self if element[key] not in compare_targets])  # type: ignore[index]

        if isinstance(key, FunctionType):
            return ExList([element for element in self if key(element) not in compare_targets])

        return ExList([element for element in self if key.fget(element) not in compare_targets])  # type: ignore[attr-defined]

    def extract_duplicates(self, other: ExList[T]) -> ExList[T]:
        """
        Returns a list of objects that are in both the current object and the given object.

        Args:
            compare_ex_list (ExList): The object to compare the current object to.

        Returns:
            ExList: A list of objects that are in both the current object and the given object. If no objects are found
                or the object is empty, an empty ExList is returned.

        Examples:
            The following example demonstrates how to use the `extract_duplicates` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ex_list_2 = ExList([{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.extract_duplicates(ex_list_2)
            [{'name': 'Bob', 'age': 30}]
        """
        return ExList([element for element in self if element in other])

    def is_duplicate(self) -> bool:
        """
        Returns `True` if there are any duplicates in the current object, `False` otherwise.

        Returns:
            bool: `True` if there are any duplicates in the current object, `False` otherwise.

        Examples:
            The following example demonstrates how to use the `is_duplicate` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Alice', 'age': 25}])
            >>> ex_list_1.is_duplicate()
            True

            >>> ex_list_2 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_2.is_duplicate()
            False
        """
        if not self:
            return False

        tmp_ex_list: ExList[T] = copy.deepcopy(self)

        for _ in range(len(tmp_ex_list)):
            if tmp_ex_list.pop() in tmp_ex_list:
                return True

        return False

    def one(self) -> T | None:
        """
        Returns the first object in the current object. If the object is empty, `None` is returned.

        Returns:
            T or None: The first object in the current object, or `None` if the object is empty.

        Examples:
            The following example demonstrates how to use the `one` method to return the first object in an ExList:

            >>> ex_list_1 = ExList([1, 2, 3])
            >>> ex_list_1.one()
            1

            The following example demonstrates how to use the `one` method to return `None` when the object is empty:

            >>> ex_list_2 = ExList([])
            >>> ex_list_2.one()
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
            The following example demonstrates how to use the `first` method to return the first object in an ExList:

            >>> ex_list_1 = ExList([1, 2, 3])
            >>> ex_list_1.first()
            1

        """
        return self[0]

    def to_dict(self, key: FunctionType | property | Hashable) -> dict[Hashable, T]:
        """
        Converts the current object to a dictionary, using the given key as the dictionary key.

        Args:
            key (FunctionType | property | Hashable): The key to use as the dictionary key.

        Returns:
            dict: A dictionary of objects, using the given key as the dictionary key.

        Examples:
            The following example demonstrates how to use the `to_dict` method to convert an ExList of dictionaries to a
            dictionary:

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ex_list_1.to_dict('name')
            {'Alice': {'name': 'Alice', 'age': 25}, 'Bob': {'name': 'Bob', 'age': 30}}

            The following example demonstrates how to use the `to_dict` method to convert an ExList of lists to a
            dictionary:

            >>> ex_list_2 = ExList([['Alice', 25], ['Bob', 30]])
            >>> ex_list_2.to_dict(0)
            {'Alice': ['Alice', 25], 'Bob': ['Bob', 30]}

            The following example demonstrates how to use the `to_dict` method to convert an ExList of objects to a
            dictionary:

            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30)])
            >>> ex_list_3.to_dict(Person.name)
            {'Alice': Person('Alice', 25), 'Bob': Person('Bob', 30)}
        """
        if not self:
            return {}

        if self.__is_indexable():
            return self.__to_dict_from_indexable_object(key)

        if isinstance(key, FunctionType):
            return {key(element): element for element in self}

        return {key.fget(element): element for element in self}  # type: ignore[attr-defined]

    def __to_dict_from_indexable_object(self, key: Hashable) -> dict[Hashable, T]:
        return {element[key]: element for element in self}  # type: ignore[index]

    def to_dict_with_complex_keys(self, keys: list[FunctionType] | list[property] | list[Hashable]) -> dict[tuple[Any, ...], T]:
        """
        Returns a dictionary of the elements in the `ExList` with complex keys.

        Args:
            keys (list[Hashable]): A list of the keys for the dictionary.

        Returns:
            dict[tuple[Any, ...], T]: A dictionary of the elements in the `ExList` with complex keys.

        Examples:
            The following example demonstrates how to use the `to_dict_with_complex_keys` method.

            >>> people = ExList([Person('Alice', 30), Person('Bob', 25), Person('Charlie', 35), Person('David', 30)])
            >>> people.to_dict_with_complex_keys([Person.name, Person.age])
            {('Alice', 30): Person('Alice', 30),
            ('Bob', 25): Person('Bob', 25),
            ('Charlie', 35): Person('Charlie', 35),
            ('David', 30): Person('David', 30)}
        """

        if not self:
            return {}

        if self.__is_indexable():
            return self.__to_dict_with_complex_keys_from_indexable_object(keys)  # type: ignore[arg-type]

        return self.__to_dict_with_complex_keys_from_others(keys)  # type: ignore[arg-type]

    def __to_dict_with_complex_keys_from_indexable_object(self, keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        return {tuple(element[key] for key in keys): element for element in self}  # type: ignore[index]

    def __to_dict_with_complex_keys_from_others(self, keys: list[FunctionType | property]) -> dict[tuple[Any, ...], T]:
        return {tuple([key(element) if isinstance(key, FunctionType) else key.fget(element) for key in keys]): element for element in self}  # type: ignore[misc]
