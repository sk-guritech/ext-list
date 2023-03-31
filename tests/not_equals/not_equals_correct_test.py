from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    assert ex_list_1.not_equals('a', 1) == [{'a': 3, 'b': 4}, {'a': 5, 'b': 6}]

    ex_list_2 = ExList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    assert ex_list_2.not_equals('a', False) == [{'a': True, 'b': False}, {'a': True, 'b': False}]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ex_list_3 = ExList([alice, bob, charlie])
    assert ex_list_3.not_equals('name', 'alice') == [bob, charlie]
    assert ex_list_3.not_equals('age', 30) == [alice, charlie]
    assert ex_list_3.not_equals(Person.introduce, 'alice is 25 years old.') == [bob, charlie]
    assert ex_list_3.not_equals('introduce', 'alice is 25 years old.') == [bob, charlie]
    assert ex_list_3.not_equals(Person.get_age_n_years_ago, 20, 5) == [bob, charlie]
    assert ex_list_3.not_equals('get_age_n_years_ago', 20, 5) == [bob, charlie]


def test_reference_getset_discriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.not_equals(int.real, 1) == [2, 3]


def test_reference_method_discriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.not_equals(int.bit_length, 2) == [1]
