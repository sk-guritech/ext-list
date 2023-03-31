from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    assert ex_list_1.not_in_('a', [1, 2]) == [{'a': 3}]

    ex_list_2 = ExList([{'a': True}, {'a': False}, {'a': True}])
    assert ex_list_2.not_in_('a', [True]) == [{'a': False}]

    alice = Person('alice', 25)
    bob = Person('bob', 30)
    charlie = Person('charlie', 35)

    ex_list_3 = ExList([alice, bob, charlie])
    assert ex_list_3.not_in_(Person.age, [30, 35]) == [alice]
    assert ex_list_3.not_in_('age', [30, 35]) == [alice]
    assert ex_list_3.not_in_(Person.introduce, ['alice is 25 years old.']) == [bob, charlie]
    assert ex_list_3.not_in_('introduce', ['alice is 25 years old.']) == [bob, charlie]
    assert ex_list_3.not_in_(Person.get_age_n_years_ago, [25, 30], 5) == [alice]
    assert ex_list_3.not_in_('get_age_n_years_ago', [25, 30], 5) == [alice]


def test_reference_getset_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.not_in_(int.real, [1]) == [2, 3]


def test_reference_method_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.not_in_(int.bit_length, [2]) == [1]
