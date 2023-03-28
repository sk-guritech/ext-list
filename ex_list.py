from __future__ import annotations

import copy
from typing import Any
from typing import Hashable
from typing import Iterable
from typing import SupportsIndex
from typing import TypeVar
from types import FunctionType

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

    def extract(self, key: FunctionType | property | Hashable) -> ExList[Any]:
        """
        Extracts and returns a list of values associated with the given key from the objects.

        Args:
            key (Hashable): The key to extract values for. This can be a string or a hashable object.
            execute_callable (bool, optional): If True, and the value associated with the key is callable,
                the callable will be executed and its result will be returned. If False (default), callable
                values will be returned as is.

        Returns:
            ExList: A list of values associated with the given key. If no values are found or the object
                is empty, an empty ExList is returned.

        Raises:
            TypeError: If the object is not a list or a tuple of dictionaries or lists, or if the key is
                not a string or a hashable object.

        Examples:
            The following example demonstrates how to use the 'extract' method.

            >>> ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
            >>> ex_list_1.extract('a')
            [1, 2, 3]

            >>> ex_list_2 = ExList([[1, 2], [3, 4], [5, 6]])
            >>> ex_list_2.extract(0)
            [1, 3, 5]

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.name = name
            ...         self.age = age
            ...
            ...     def say(self):
            ...         print(f'{self.name} is {self.age} years old.')
            ...
            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.extract('name')
            ['Alice', 'Bob', 'Charlie']

            The following example demonstrates how to use the 'execute_callable' option.

            >>> ex_list_4 = ExList([Person('Alice', 25)])
            >>> ex_list_4.extract('say', execute_callable=True)
            ['Alice is 25 years old.']
        """
        if not self:
            return ExList()

        if isinstance(key, FunctionType):
            return ExList([key(element) for element in self])

        if isinstance(key, property):
            return ExList([key.fget(element) for element in self])  # type: ignore[arg-type]

        return ExList([element[key] for element in self])  # type: ignore[attr-defined]

    def equals(self, key: Hashable, compare_target: Any) -> ExList[T]:
        """
        Returns a list of objects that have the given key set to the given value.

        Args:
            key (Hashable): The key to search for. This can be a string or a hashable object.
            compare_target (Any): The value to compare the objects' values to.

        Returns:
            ExList: A list of objects that have the given key set to the given value. If no objects are found or the object
                is empty, an empty ExList is returned.

        Raises:
            TypeError: If the object is not a list or a tuple of dictionaries or lists, or if the key is
                not a string or a hashable object.

        Examples:
            The following example demonstrates how to use the `equals` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.equals('age', 25)
            [{'name': 'Alice', 'age': 25}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.equals('graduated', None)
            [{'name': 'Alice', 'graduated': None}]

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.name = name
            ...         self.age = age
            ...
            ...     def __repr__(self):
            ...         return f'Person({self.name}, {self.age})'
            ...
            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.equals('name', 'Alice')
            [Person(Alice, 25)]
        """
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
        """
        Returns a list of objects that do not have the given key set to the given value.

        Args:
            key (Hashable): The key to search for. This can be a string or a hashable object.
            compare_target (Any): The value to compare the objects' values to.

        Returns:
            ExList: A list of objects that do not have the given key set to the given value. If no objects are found or the
                object is empty, an empty ExList is returned.

        Raises:
            TypeError: If the object is not a list or a tuple of dictionaries or lists, or if the key is not
                a string or a hashable object.

        Examples:
            The following example demonstrates how to use the `not_equals` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.not_equals('age', 25)
            [{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.not_equals('graduated', None)
            [{'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}]

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.name = name
            ...         self.age = age
            ...
            ...     def __repr__(self):
            ...         return f'Person({self.name}, {self.age})'
            ...
            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ex_list_3.equals('age', 30)
            [Person(Bob, 30), Person(David, 30)]
        """
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
        """
        Returns a list of objects that have the given key set to one of the given values.

        Args:
            key (Hashable): The key to search for. This can be a string or a hashable object.
            compare_targets (list): A list of values to compare the objects' values to.

        Returns:
            ExList: A list of objects that have the given key set to one of the given values. If no objects are found or
                the object is empty, an empty ExList is returned.

        Raises:
            TypeError: If the object is not a list or a tuple of dictionaries or lists, or if the key is not
                a string or a hashable object.

        Examples:
            The following example demonstrates how to use the `in_` method.

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.in_('age', [25, 30])
            [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.in_('graduated', [False, True])
            [{'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}]

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.name = name
            ...         self.age = age
            ...
            ...     def __repr__(self):
            ...         return f'Person({self.name}, {self.age})'
            ...
            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.in_('age', [25, 35])
            [Person(Alice, 25), Person(Charlie, 35)]
        """
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
        """
        Returns a list of objects that do not have the given key set to any of the given values.

        Args:
            key (Hashable or str): The key to search for. This can be a string or a hashable object.
            compare_targets (list): A list of values to compare the objects' values to.

        Returns:
            ExList: A list of objects that do not have the given key set to any of the given values. If no objects are
                found or the object is empty, an empty ExList is returned.

        Raises:
            TypeError: If the object is not a list or a tuple of dictionaries or lists, or if the key is not a string
                or a hashable object.

        Examples:
            The following example demonstrates how to use the `not_in_` method:

            >>> ex_list_1 = ExList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ex_list_1.not_in_('age', [25, 30])
            [{'name': 'Charlie', 'age': 35}]

            >>> ex_list_2 = ExList([{'name': 'Alice', 'graduated': None}, {'name': 'Bob', 'graduated': False}, {'name': 'Charlie', 'graduated': True}])
            >>> ex_list_2.not_in_('graduated', [False, True])
            [{'name': 'Alice', 'graduated': None}]

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.name = name
            ...         self.age = age
            ...
            ...     def __repr__(self):
            ...         return f'Person({self.name}, {self.age})'
            ...
            >>> ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
            >>> ex_list_3.not_in_('age', [25, 35])
            [Person(Bob, 30)]
        """
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
        return ExList([element for element in self if element in compare_ex_list])

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

            >>> ex_list_1 = [1, 2, 3]
            >>> ex_list_1.one()
            1

            The following example demonstrates how to use the `one` method to return `None` when the object is empty:

            >>> ex_list_2 = []
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

            >>> ex_list_1 = [1, 2, 3]
            >>> ex_list_1.first()
            1

        """
        return self[0]

    def to_dict(self, key: Hashable) -> dict[Hashable, T]:
        """
        Converts the current object to a dictionary, using the given key as the dictionary key.

        Args:
            key (Hashable): The key to use as the dictionary key.

        Returns:
            dict: A dictionary of objects, using the given key as the dictionary key.

        Raises:
            TypeError: If the object is not a list or a dict, or if the key is not a string or a hashable object.

        Examples:
            The following example demonstrates how to use the `to_dict` method to convert an ExList of dictionaries to a
            dictionary:

            >>> ex_list_1 = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
            >>> ex_list_1.to_dict('name')
            {'Alice': {'name': 'Alice', 'age': 25}, 'Bob': {'name': 'Bob', 'age': 30}}

            The following example demonstrates how to use the `to_dict` method to convert an ExList of objects to a
            dictionary:

            >>> class Person:
            ...     def __init__(self, name, age):
            ...         self.name = name
            ...         self.age = age
            ...
            ...     def __repr__(self):
            ...         return f'Person({self.name}, {self.age})'
            ...
            >>> ex_list_2 = [Person('Alice', 25), Person('Bob', 30)]
            >>> ex_list_2.to_dict('name')
            {'Alice': Person(Alice, 25), 'Bob': Person(Bob, 30)}

            The following example demonstrates how to use the `to_dict` method to convert an ExList of lists to a
            dictionary:

            >>> ex_list_3 = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
            >>> ex_list_3.to_dict('name')
            {'Alice': {'name': 'Alice', 'age': 25}, 'Bob': {'name': 'Bob', 'age': 30}}
        """
        if not self:
            return {}

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__to_dict_from_dict_or_list(key)

        if isinstance(key, str):
            return self.__to_dict_from_others(key)

        raise TypeError

    def __to_dict_from_dict_or_list(self, key: Hashable) -> dict[Hashable, T]:
        return {element[key]: element for element in self}  # type: ignore[index]

    def __to_dict_from_others(self, key: str) -> dict[Hashable, T]:
        return {getattr(element, key): element for element in self}

    def to_dict_with_complex_keys(self, keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        """
        Returns a dictionary of the elements in the `ExList` with complex keys based on multiple attributes.

        Args:
            keys (list[Hashable]): A list of the attributes to use as keys for the dictionary.

        Returns:
            dict[tuple[Any, ...], T]: A dictionary of the elements in the `ExList` with complex keys.

        Raises:
            TypeError: If the elements in the `ExList` are not dictionaries or lists and the `keys` argument contains
                non-string values.

        Examples:
            The following example demonstrates how to use the `to_dict_with_complex_keys` method.

            >>> class Person:
            ...     def __init__(self, name, age, occupation):
            ...         self.name = name
            ...         self.age = age
            ...         self.occupation = occupation
            ...
            ...     def __repr__(self):
            ...         return f'Person(name={self.name}, age={self.age}, occupation={self.occupation})'
            ...
            >>> people = ExList([Person('Alice', 30, 'Engineer'), Person('Bob', 25, 'Teacher'),
            ...                  Person('Charlie', 35, 'Engineer'), Person('David', 30, 'Doctor')])
            >>> people.to_dict_with_complex_keys(['occupation', 'age'])
            {('Engineer', 30): Person(name=Alice, age=30, occupation=Engineer),
             ('Teacher', 25): Person(name=Bob, age=25, occupation=Teacher),
             ('Engineer', 35): Person(name=Charlie, age=35, occupation=Engineer),
             ('Doctor', 40): Person(name=David, age=40, occupation=Doctor)}
        """

        if not self:
            return {}

        if isinstance(self[0], dict) or isinstance(self[0], list):
            return self.__to_dict_with_complex_keys_from_dict_or_list(keys)

        if all([isinstance(key, str) for key in keys]):
            return self.__to_dict_with_complex_keys_from_others(keys)  # type: ignore[arg-type]

        raise TypeError

    def __to_dict_with_complex_keys_from_dict_or_list(self, keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        return {tuple(element[key] for key in keys): element for element in self}  # type: ignore[index]

    def __to_dict_with_complex_keys_from_others(self, keys: list[str]) -> dict[tuple[Any, ...], T]:
        return {tuple(getattr(element, key) for key in keys): element for element in self}
