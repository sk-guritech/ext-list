from __future__ import annotations

import copy
from types import FunctionType
from types import GetSetDescriptorType
from types import MethodDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import SupportsIndex
from typing import TypeVar

from typing_extensions import override

T = TypeVar('T')
TI = TypeVar('TI', bound=type)


class ExtList(list[T]):
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
        ExtList.__validate_all_elements_are_same_type(iterable)
        super().__init__(iterable)

    @staticmethod
    def __validate_all_elements_are_same_type(iterable: list[Any]) -> None:
        if not iterable:
            return

        allowed_type: Any = type(iterable[0])

        if not all(isinstance(element, allowed_type) for element in iterable):
            raise TypeError(
                'Expected all elements to be of the same type.',
            )

    @staticmethod
    def __validate_ext_list(iterable: Any) -> None:
        if not isinstance(iterable, ExtList):
            raise TypeError(f'Expected <class \'ExtList\'> but got {type(iterable)}')

    def __validate_same_type_element(self, element: T) -> None:
        if not isinstance(element, type(self[0])):
            raise TypeError(
                f'Expected {type(self[0])} but got {type(element)}.',
            )

    def __validate_same_type_ext_list(self, other: ExtList[T]):
        if not isinstance(self[0], type(other[0])):  # type: ignore[index]
            raise TypeError(
                f'Expected ExtList[{type(self[0])}] but got ExtList[{type(other[0])}].',  # type: ignore[index]
            )

    def __is_indexable(self) -> bool:
        return hasattr(self[0], '__getitem__')

    @staticmethod
    def __get_value_by_function(element: T, func: FunctionType, *args: Any) -> Any:
        return func(element, *args)

    @staticmethod
    def __get_value_by_index(element: T, index: SupportsIndex | Hashable) -> Any:
        return element[index]  # type: ignore

    @staticmethod
    def __get_value_by_property(element: T, prop: property) -> Any:
        return prop.__get__(element)  # type: ignore[misc]

    @staticmethod
    def __get_value_by_attr_name(element: T, attr_name: str, *args: Any) -> Any:
        object = getattr(element, attr_name)

        if callable(object):
            return object(*args)

        return object

    def __determine_get_value_method(self, key: FunctionType | property | str | Hashable) -> Callable[[T, Any], Any]:
        if self.__is_indexable():
            return ExtList.__get_value_by_index

        match key:
            case FunctionType() | MethodDescriptorType():
                return ExtList.__get_value_by_function

            case property() | GetSetDescriptorType():
                return ExtList.__get_value_by_property

            case _:
                return ExtList.__get_value_by_attr_name

    @ override
    def __add__(self, other: ExtList[T]) -> ExtList[T]:  # type: ignore[override]
        self.__validate_ext_list(other)

        if not self:
            return other

        if not other:
            return self

        self.__validate_same_type_ext_list(other)

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

        self.__validate_same_type_ext_list(other)

        super().__iadd__(other)

        return self

    @ override
    def append(self, element: T) -> None:
        if not self:
            super().append(element)
            return

        self.__validate_same_type_element(element)

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

        self.__validate_same_type_ext_list(other)

        super().extend(other)

    @ override
    def insert(self, index: SupportsIndex, element: T) -> None:
        if not self:
            super().insert(index, element)
            return

        self.__validate_same_type_element(element)

        super().insert(index, element)

    def extract(self, key: FunctionType | property | str | Hashable, *args: Any) -> ExtList[Any]:
        """
        Extracts and returns a list of values associated with the given key from the objects.

        Args:
            key (FunctionType | property | str | Hashable): The key to extract values for. If the key is function,
                the callable will be executed and its result will be returned.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList: A list of values associated with the given key. If no values are found or the object
                is empty, an empty ExtList is returned.

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
            return ExtList()

        get_value_method: Callable[[T, Any], Any] = self.__determine_get_value_method(key)

        return ExtList([get_value_method(element, key, *args) for element in self])  # type: ignore[arg-type]

    def equals(self, key: FunctionType | property | str | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that have the given key set to the given value.

        Args:
            key (FunctionType | property | str | Hashable): The key to search for.
            compare_target (Any): The value to compare the objects' values to.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList: A list of objects that have the given key set to the given value. If no objects are found or the object
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
        if not self:
            return ExtList()

        get_value_method: Callable[[T, Any], Any] = self.__determine_get_value_method(key)

        if compare_target in {None, False, True}:
            return ExtList([element for element in self if get_value_method(element, key, *args) is compare_target])  # type: ignore[arg-type]

        return ExtList([element for element in self if get_value_method(element, key, *args) == compare_target])  # type: ignore[arg-type]

    def not_equals(self, key: FunctionType | property | Hashable, compare_target: Any, *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that do not have the given key set to the given value.

        Args:
            key (FunctionType | property | str | Hashable): The key to search for.
            compare_target (Any): The value to compare the objects' values to.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList: A list of objects that do not have the given key set to the given value. If no objects are found or the
                object is empty, an empty ExtList is returned.

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
        if not self:
            return ExtList()

        get_value_method: Callable[[T, Any], Any] = self.__determine_get_value_method(key)

        if compare_target in {None, False, True}:
            return ExtList([element for element in self if get_value_method(element, key, *args) is not compare_target])  # type: ignore[arg-type]

        return ExtList([element for element in self if get_value_method(element, key, *args) != compare_target])  # type: ignore[arg-type]

    def in_(self, key: FunctionType | property | str | Hashable, compare_targets: list[Any], *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that have the given key set to one of the given values.

        Args:
            key (FunctionType | property | str | Hashable): The key to search for.
            compare_targets (list): A list of values to compare the objects' values to.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList: A list of objects that have the given key set to one of the given values. If no objects are found or
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
        if not self:
            return ExtList()

        get_value_method: Callable[[T, Any], Any] = self.__determine_get_value_method(key)

        return ExtList([element for element in self if get_value_method(element, key, *args) in compare_targets])  # type: ignore[arg-type]

    def not_in_(self, key: FunctionType | property | str | Hashable, compare_targets: list[Any], *args: Any) -> ExtList[T]:
        """
        Returns a list of objects that do not have the given key set to any of the given values.

        Args:
            key (FunctionType | property | str | Hashable): The key to search for.
            compare_targets (list): A list of values to compare the objects' values to.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            ExtList: A list of objects that do not have the given key set to any of the given values. If no objects are
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
        if not self:
            return ExtList()

        get_value_method: Callable[[T, Any], Any] = self.__determine_get_value_method(key)

        return ExtList([element for element in self if get_value_method(element, key, *args) not in compare_targets])  # type: ignore[arg-type]

    def extract_duplicates(self, other: ExtList[T]) -> ExtList[T]:
        """
        Returns a list of objects that are in both the current object and the given object.

        Args:
            compare_ext_list (ExtList): The object to compare the current object to.

        Returns:
            ExtList: A list of objects that are in both the current object and the given object. If no objects are found
                or the object is empty, an empty ExtList is returned.

        Examples:
            The following example demonstrates how to use the `extract_duplicates` method.

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ext_list_2 = ExtList([{'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])
            >>> ext_list_1.extract_duplicates(ext_list_2)
            [{'name': 'Bob', 'age': 30}]
        """
        return ExtList([element for element in self if element in other])

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

        tmp_ext_list: ExtList[T] = copy.deepcopy(self)

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

    def to_dict(self, key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, T]:
        """
        Converts the current object to a dictionary, using the given key as the dictionary key.

        Args:
            key (FunctionType | property | str | Hashable): The key to use as the dictionary key.
            *args Any: If key is a function, the arguments will be passed to the function.

        Returns:
            dict: A dictionary of objects, using the given key as the dictionary key.

        Examples:
            The following example demonstrates how to use the `to_dict` method to convert an ExtList of dictionaries to a
            dictionary:

            >>> ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
            >>> ext_list_1.to_dict('name')
            {'Alice': {'name': 'Alice', 'age': 25}, 'Bob': {'name': 'Bob', 'age': 30}}

            The following example demonstrates how to use the `to_dict` method to convert an ExtList of lists to a
            dictionary:

            >>> ext_list_2 = ExtList([['Alice', 25], ['Bob', 30]])
            >>> ext_list_2.to_dict(0)
            {'Alice': ['Alice', 25], 'Bob': ['Bob', 30]}

            The following example demonstrates how to use the `to_dict` method to convert an ExtList of objects to a
            dictionary:

            >>> ext_list_3 = ExtList([Person('Alice', 25), Person('Bob', 30)])
            >>> ext_list_3.to_dict(Person.name)
            {'Alice': Person('Alice', 25), 'Bob': Person('Bob', 30)}

            >>> ext_list_3.to_dict(Person.get_age_n_years_ago, 5)
            {20: Person('Alice', 25), 25: Person('Bob', 30)}
        """
        if not self:
            return {}

        get_value_method: Callable[[T, Any], Any] = self.__determine_get_value_method(key)

        return {get_value_method(element, key, *args): element for element in self}  # type: ignore[arg-type]

    def to_dict_with_complex_keys(self, keys: list[FunctionType | property | str] | list[Hashable], arg_tuples: tuple[tuple[Any, ...], ...] = tuple()) -> dict[tuple[Any, ...], T]:
        """
        Returns a dictionary of the elements in the `ExtList` with complex keys.

        Args:
            keys (list[FunctionType | property | str] | list[Hashable]): A list of the keys for the dictionary.
            arg_tuples (tuple[tuple[Any,...],...]): A list of tuples of the arguments. If key is a function, the arguments will be passed to the function.

        Returns:
            dict[tuple[Any, ...], T]: A dictionary of the elements in the `ExtList` with complex keys.

        Examples:
            The following example demonstrates how to use the `to_dict_with_complex_keys` method.

            >>> ext_list_1 = ExtList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35), Person('David', 30)])
            >>> ext_list_1.to_dict_with_complex_keys([Person.name, Person.age])
            {('Alice', 25): Person('Alice', 25),
             ('Bob', 30): Person('Bob', 30),
             ('Charlie', 35): Person('Charlie', 35),
             ('David', 30): Person('David', 30)}

            >>> ext_list_1.to_dict_with_complex_keys(['name', Person.introduce, Person.get_age_n_years_ago], ((), (), (5,)))
            {('Alice', 'Alice is 25 years old.', 20): Person('Alice', 25),
             ('Bob', 'Bob is 30 years old.', 25): Person('Bob', 30),
             ('Charlie', 'Charlie is 35 years old.', 30): Person('Charlie', 35),
             ('David', 'David is 30 years old.', 25): Person('David', 30)}
        """

        if not self:
            return {}

        if self.__is_indexable():
            return self.__to_dict_with_complex_keys_from_indexable_object(keys)  # type: ignore[arg-type]

        return self.__to_dict_with_complex_keys_from_others(keys, arg_tuples)  # type: ignore[arg-type]

    def __to_dict_with_complex_keys_from_indexable_object(self, keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
        return {tuple(element[key] for key in keys): element for element in self}  # type: ignore[index]

    def __to_dict_with_complex_keys_from_others(self, keys: list[FunctionType | property | str], arg_tuples: tuple[tuple[Any, ...]]) -> dict[tuple[Any, ...], T]:
        result: dict[tuple[Any, ...], T] = {}

        if not arg_tuples:
            arg_tuples = tuple(tuple() for _ in range(len(keys)))

        for element in self:
            tupled_key: tuple[Any, ...] = self.__generate_tupled_key(keys, element, arg_tuples)
            result[tupled_key] = element

        return result

    def __generate_tupled_key(self, keys: list[FunctionType | property | str], element: T, arg_tuples: tuple[Any]) -> tuple[Any, ...]:
        tupled_key: tuple[Any, ...] = tuple()

        for key, arg_tuple in zip(keys, arg_tuples):
            get_value_method = self.__determine_get_value_method(key)
            tupled_key += (get_value_method(element, key, *arg_tuple),)

        return tupled_key

    def map(self, function: FunctionType | type, *args: Any) -> ExtList[Any]:
        """
        Apply a function or constructor to each element.

        Args:
            function (FunctionType | type): The function to apply to each element.
            *args (Any): Additional arguments to pass to the function.

        Returns:
            ExtList[Any]: A new ExtList containing the mapped values.

        Examples:
            The following example demonstrates how to use the `map` method.

            >>> ext_list_1 = ExtList([1, 2, 3])
            >>> ext_list_1.map(float)
            [1.0, 2.0, 3.0]
        """
        return ExtList([function(element, *args) for element in self])

    def dicts_to_instances(self: ExtList[dict[str, Any]], type_: TI) -> ExtList[TI]:
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
        """
        return ExtList([type_(**element) for element in self])
