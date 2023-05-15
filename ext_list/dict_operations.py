from __future__ import annotations

import copy
from types import FunctionType
from types import GetSetDescriptorType
from types import MethodDescriptorType
from typing import Any
from typing import Callable
from typing import Hashable
from typing import List
from typing import TypeVar

from ext_list import base

T = TypeVar('T')
TI = TypeVar('TI')


class DictOperation(List[T]):
    def to_dict(self, key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, T]:
        """
        Converts the current object to a dictionary, using the given key as the dictionary key.

        Args:
            key (FunctionType | property | str | Hashable): The key to use as the dictionary key. If the key is function,
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
        """
        if not self:
            return {}

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        return {get_value_method(element, key, *args): element for element in self}

    def to_dict_list(self, keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> DictOperation[dict[str | Hashable, T]]:
        """
        Converts the objects into a list of dictionaries, where each dictionary contains the specified keys
        and their corresponding values from the object.

        Args:
            keys (list[FunctionType | property | str | Hashable]): A list of keys to include in the dictionaries. Each key can
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

        """
        def __to_dict_list_from_indexable_object(elements: list[T], keys: list[Hashable]) -> DictOperation[dict[str | Hashable, T]]:
            return DictOperation([{key: element[key] for key in keys} for element in elements])   # type: ignore[attr-defined]

        def __to_dict_list_from_others(
            elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]],
        ) -> DictOperation[dict[str | Hashable, T]]:
            if not arg_tuples:
                arg_tuples = list(tuple() for _ in range(len(keys)))

            result: DictOperation[dict[str | Hashable, T]] = DictOperation()

            for element in elements:
                row: dict[str | Hashable, T] = __generate_dict_from_specified_keys(elements, keys, arg_tuples, element)

                result.append(row)

            return result

        def __generate_dict_from_specified_keys(
            elements: list[T], keys: list[FunctionType | property | str | Hashable], arg_tuples: list[tuple[Any, ...]], element: T,
        ) -> dict[str | Hashable, Any]:
            result: dict[str | Hashable, Any] = {}

            for arg_tuple, key in zip(arg_tuples, keys):
                get_value_method = base.determine_get_value_method(elements, key)

                if isinstance(key, property):
                    dict_key: str | Hashable = key.fget.__name__  # type: ignore[attr-defined]

                elif isinstance(key, FunctionType) or isinstance(key, MethodDescriptorType) or isinstance(key, GetSetDescriptorType):
                    dict_key = key.__name__

                elif isinstance(key, str):
                    dict_key = key

                else:
                    dict_key = key

                result[dict_key] = get_value_method(element, key, *arg_tuple)  # type: ignore[assignment]

            return result

        if not self:
            return DictOperation()

        if base.is_indexable(self):
            return __to_dict_list_from_indexable_object(self, keys)

        return __to_dict_list_from_others(self, keys, arg_tuples)

    def to_dict_with_complex_keys(self, keys: list[FunctionType | property | str] | list[Hashable], arg_tuples: list[tuple[Any, ...]] = []) -> dict[tuple[Any, ...], T]:
        """
        Returns a dictionary of the objects in the `ExtList` with complex keys.

        Args:
            keys (List[FunctionType | property | str] | List[Hashable]): A list of the keys for the dictionary.
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
        """
        def __to_dict_with_complex_keys_from_indexable_object(elements: list[T], keys: list[Hashable]) -> dict[tuple[Any, ...], T]:
            return {tuple(element[key] for key in keys): element for element in elements}  # type: ignore[index]

        def __to_dict_with_complex_keys_from_others(elements: list[T], keys: list[FunctionType | property | str], arg_tuples: list[tuple[Any, ...]]) -> dict[tuple[Any, ...], T]:
            result: dict[tuple[Any, ...], T] = {}

            if not arg_tuples:
                arg_tuples = list(tuple() for _ in range(len(keys)))

            for element in elements:
                tupled_key: tuple[Any, ...] = __generate_tupled_key(elements, keys, element, arg_tuples)
                result[tupled_key] = element

            return result

        def __generate_tupled_key(elements: list[T], keys: list[FunctionType | property | str], element: T, arg_tuples: list[tuple[Any, ...]]) -> tuple[Any, ...]:
            tupled_key: tuple[Any, ...] = tuple()

            for key, arg_tuple in zip(keys, arg_tuples):
                get_value_method = base.determine_get_value_method(elements, key)
                tupled_key += (get_value_method(element, key, *arg_tuple),)

            return tupled_key

        if not self:
            return {}

        if base.is_indexable(self):
            return __to_dict_with_complex_keys_from_indexable_object(self, keys)  # type: ignore[arg-type]

        return __to_dict_with_complex_keys_from_others(self, keys, arg_tuples)  # type: ignore[arg-type]

    def dicts_to_instances(self, type_: TI) -> DictOperation[TI]:
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
        return [type_(**element) for element in self]  # type: ignore[assignment]

    def group_by_key(self, key: FunctionType | property | str | Hashable, *args: Any) -> dict[Hashable, DictOperation[T]]:  # type: ignore
        """Groups the objects of the list by a specified key.

        Args:
            key (FunctionType | property | str | Hashable): The key to group the objects by. This can be
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

        """
        result: dict[Hashable, DictOperation[T]] = {}

        get_value_method: Callable[[T, Any], Any] = base.determine_get_value_method(self, key)

        for element in self:
            group_key: Hashable = get_value_method(element, key, *args)

            if group_key in result:
                result[group_key].append(element)  # type: ignore[attr-defined]

            else:
                result[group_key] = list([element])  # type: ignore[attr-defined]

        return result

    def rename_keys(self, rename_keys: dict[Hashable, Hashable]) -> DictOperation[T]:
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
        """
        if not self:
            return DictOperation()

        if not base.is_indexable(self):
            raise TypeError

        result: DictOperation[T] = DictOperation()

        for element in copy.deepcopy(self):
            for from_key, to_key in rename_keys.items():
                element[to_key] = element.pop(from_key)  # type: ignore[attr-defined]

            result.append(element)  # type: ignore[assignment]

        return result
