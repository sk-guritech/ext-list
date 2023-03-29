from __future__ import annotations

import pytest

from ex_list import ExList


class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def introduce(self):
        return f'{self.name} is {self.age} years old.'

    def get_age_n_years_old(self, n: int) -> int:
        return self.age - n

    @ property
    def name(self):
        return self.__name

    @ property
    def age(self):
        return self.__age

    def __repr__(self):
        return f'Person(\'{self.name}\', {self.age})'


def test_init():
    assert ExList([1, 2, 3]) == [1, 2, 3]


def test_init_raise_type_error_by_assign_multiple_types():
    with pytest.raises(TypeError):
        ExList([1, '2'])


def test_add():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([4, 5, 6])

    assert ex_list_1 + ExList[int]([]) == [1, 2, 3]
    assert ExList[int]([]) + ex_list_1 == [1, 2, 3]
    assert ex_list_1 + ex_list_2 == [1, 2, 3, 4, 5, 6]


def test_add_raise_type_error_by_operating_between_diffent_types():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList(['4', '5', '6'])

    with pytest.raises(TypeError):
        ex_list_1 + ex_list_2


def test_iadd():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([4, 5, 6])

    ex_list_1 += ex_list_2

    assert ex_list_1 == [1, 2, 3, 4, 5, 6]
    assert ex_list_2 == [4, 5, 6]


def test_iadd_raise_type_error_by_operating_between_diffent_types():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList(['4', '5', '6'])

    with pytest.raises(TypeError):
        ex_list_1 += ex_list_2


def test_iadd_raise_type_error_by_assign_invalid_object():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = [4, 5, 6]

    with pytest.raises(TypeError):
        ex_list_1 += ex_list_2


def test_append():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_1.append(4)

    assert ex_list_1 == [1, 2, 3, 4]


def test_append_raise_type_error_by_assign_different_type():
    ex_list_1 = ExList([1, 2, 3])

    with pytest.raises(TypeError):
        ex_list_1.append('4')


def test_extend():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_1.extend(ExList([4]))

    assert ex_list_1 == [1, 2, 3, 4]


def test_extend_raise_type_error_by_assign_invalid_object():
    ex_list_1 = ExList([1, 2, 3])

    with pytest.raises(TypeError):
        ex_list_1.extend([4])


def test_extend_raise_type_error_by_assign_different_type():
    ex_list_1 = ExList([1, 2, 3])

    with pytest.raises(TypeError):
        ex_list_1.extend(['a', 'b'])


def test_insert():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_1.insert(0, 0)

    assert ex_list_1 == [0, 1, 2, 3]


def test_insert_raise_type_error_by_assign_different_type():
    ex_list_1 = ExList([1, 2, 3])

    with pytest.raises(TypeError):
        ex_list_1.insert(0, '0')


def test_extract_for_dict():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    assert ex_list_1.extract('a') == [1, 2, 3]


def test_extract_for_list():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    assert ex_list_1.extract(1) == [2, 4, 6]


def test_extract_for_others():
    ex_list_1 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.extract(Person.name) == ['Alice', 'Bob', 'Charlie']
    assert ex_list_1.extract('name') == ['Alice', 'Bob', 'Charlie']
    assert ex_list_1.extract(Person.introduce) == ['Alice is 25 years old.', 'Bob is 30 years old.', 'Charlie is 35 years old.']
    assert ex_list_1.extract(Person.get_age_n_years_old, 5) == [20, 25, 30]


def test_extract_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.extract('b')


def test_extract_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.extract(2)


def test_equals():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    ex_list_2 = ExList([{'a': True}, {'a': False}, {'a': True}])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.equals('a', 1) == [{'a': 1}]
    assert ex_list_2.equals('a', True) == [{'a': True}, {'a': True}]
    assert ex_list_3.equals(Person.age, 25) == [ex_list_3[0]]
    assert ex_list_3.equals(Person.get_age_n_years_old, 20, 5) == [ex_list_3[0]]
    assert ex_list_3.equals('get_age_n_years_old', 20, 5) == [ex_list_3[0]]
    assert ex_list_3.equals('age', 25) == [ex_list_3[0]]


def test_equals_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.equals('b', 1)


def test_equals_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.equals(2, 1)


def test_not_equals():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    ex_list_2 = ExList([{'a': True}, {'a': False}, {'a': True}])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.not_equals('a', 1) == [{'a': 2}, {'a': 3}]
    assert ex_list_2.not_equals('a', True) == [{'a': False}]
    assert ex_list_3.not_equals(Person.age, 25) == [ex_list_3[1], ex_list_3[2]]
    assert ex_list_3.not_equals(Person.get_age_n_years_old, 20, 5) == [ex_list_3[1], ex_list_3[2]]
    assert ex_list_3.not_equals('get_age_n_years_old', 20, 5) == [ex_list_3[1], ex_list_3[2]]
    assert ex_list_3.not_equals('age', 25) == [ex_list_3[1], ex_list_3[2]]


def test_not_equals_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.not_equals('b', 1)


def test_not_equals_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.not_equals(2, 1)


def test_in_():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    ex_list_2 = ExList([{'a': True}, {'a': False}, {'a': True}])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.in_('a', [1, 2]) == [{'a': 1}, {'a': 2}]
    assert ex_list_2.in_('a', [True]) == [{'a': True}, {'a': True}]
    assert ex_list_3.in_(Person.age, [30, 35]) == [ex_list_3[1], ex_list_3[2]]
    assert ex_list_3.in_(Person.get_age_n_years_old, [25, 30], 5) == [ex_list_3[1], ex_list_3[2]]
    assert ex_list_3.in_('get_age_n_years_old', [25, 30], 5) == [ex_list_3[1], ex_list_3[2]]
    assert ex_list_3.in_('age', [30, 35]) == [ex_list_3[1], ex_list_3[2]]


def test_in_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.in_('b', 1)


def test_in_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.in_(2, 1)


def test_not_in_():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    ex_list_2 = ExList([{'a': True}, {'a': False}, {'a': True}])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.not_in_('a', [1, 2]) == [{'a': 3}]
    assert ex_list_2.not_in_('a', [True]) == [{'a': False}]
    assert ex_list_3.not_in_(Person.age, [30, 35]) == [ex_list_3[0]]
    assert ex_list_3.not_in_(Person.get_age_n_years_old, [25, 30], 5) == [ex_list_3[0]]
    assert ex_list_3.not_in_('get_age_n_years_old', [25, 30], 5) == [ex_list_3[0]]
    assert ex_list_3.not_in_('age', [30, 35]) == [ex_list_3[0]]


def test_not_in_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.not_in_('b', [1])


def test_not_in_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.not_in_(2, [1])


def test_extract_duplicates():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([2, 3, 4])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])
    ex_list_4 = ExList([Person('Alice', 35), Person('Bob', 40), Person('Charlie', 45)])

    assert ex_list_1.extract_duplicates(ex_list_2) == [2, 3]
    assert ex_list_3.extract_duplicates(ex_list_4) == []


def test_is_duplicate():
    ex_list_1 = ExList([1, 2, 3, 3])
    ex_list_2 = ExList([1, 2, 3, 4])

    assert ex_list_1.is_duplicate() is True
    assert ex_list_2.is_duplicate() is False


def test_one():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([])

    assert ex_list_1.one() == 1
    assert ex_list_2.one() is None


def test_first():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.first() == 1


def test_first_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([])

    with pytest.raises(IndexError):
        ex_list_1.first()


def test_to_dict():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    ex_list_2 = ExList([[1, 2], [3, 4], [5, 6]])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.to_dict('a') == {1: {'a': 1}, 2: {'a': 2}, 3: {'a': 3}}
    assert ex_list_2.to_dict(0) == {1: [1, 2], 3: [3, 4], 5: [5, 6]}
    assert ex_list_3.to_dict(Person.name) == {'Alice': ex_list_3[0], 'Bob': ex_list_3[1], 'Charlie': ex_list_3[2]}
    assert ex_list_3.to_dict(Person.get_age_n_years_old, 5) == {20: ex_list_3[0], 25: ex_list_3[1], 30: ex_list_3[2]}
    assert ex_list_3.to_dict('name') == {'Alice': ex_list_3[0], 'Bob': ex_list_3[1], 'Charlie': ex_list_3[2]}


def test_to_dict_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.to_dict('b')


def test_to_dict_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.to_dict(2)


def test_to_dict_with_complex_keys():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 2, 'b': 3}])
    ex_list_2 = ExList([[1, 2], [3, 4], [5, 6]])
    ex_list_3 = ExList([Person('Alice', 25), Person('Bob', 30), Person('Charlie', 35)])

    assert ex_list_1.to_dict_with_complex_keys(['a', 'b']) == {
        (1, 2): {'a': 1, 'b': 2},
        (1, 3): {'a': 1, 'b': 3},
        (2, 3): {'a': 2, 'b': 3},
    }

    assert ex_list_2.to_dict_with_complex_keys([0, 1]) == {
        (1, 2): [1, 2],
        (3, 4): [3, 4],
        (5, 6): [5, 6],
    }

    assert ex_list_3.to_dict_with_complex_keys([Person.name, Person.age]) == {
        ('Alice', 25): ex_list_3[0],
        ('Bob', 30): ex_list_3[1],
        ('Charlie', 35): ex_list_3[2],
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', Person.age]) == {
        ('Alice', 25): ex_list_3[0],
        ('Bob', 30): ex_list_3[1],
        ('Charlie', 35): ex_list_3[2],
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', Person.introduce, Person.age]) == {
        ('Alice', 'Alice is 25 years old.', 25): ex_list_3[0],
        ('Bob', 'Bob is 30 years old.', 30): ex_list_3[1],
        ('Charlie', 'Charlie is 35 years old.', 35): ex_list_3[2],
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', Person.introduce, Person.get_age_n_years_old], ((), (), (5,))) == {
        ('Alice', 'Alice is 25 years old.', 20): ex_list_3[0],
        ('Bob', 'Bob is 30 years old.', 25): ex_list_3[1],
        ('Charlie', 'Charlie is 35 years old.', 30): ex_list_3[2],
    }


def test_to_dict_with_complex_keys_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 2, 'b': 3}])

    with pytest.raises(KeyError):
        ex_list_1.to_dict_with_complex_keys(['a', 'c'])


def test_to_dict_with_complex_keys_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.to_dict_with_complex_keys([1, 2])
