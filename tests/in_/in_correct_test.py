from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    assert ex_list_1.in_('a', [1, 2]) == [{'a': 1}, {'a': 2}]

    ex_list_2 = ExList([{'a': True}, {'a': False}, {'a': True}])
    assert ex_list_2.in_('a', [True]) == [{'a': True}, {'a': True}]

    alice = Person('alice', 25)
    bob = Person('bob', 30)
    charlie = Person('charlie', 35)

    ex_list_3 = ExList([alice, bob, charlie])
    assert ex_list_3.in_(Person.age, [30, 35]) == [bob, charlie]
    assert ex_list_3.in_('age', [30, 35]) == [bob, charlie]
    assert ex_list_3.in_(Person.introduce, ['alice is 25 years old.']) == [alice]
    assert ex_list_3.in_('introduce', ['alice is 25 years old.']) == [alice]
    assert ex_list_3.in_(Person.get_age_n_years_ago, [25, 30], 5) == [bob, charlie]
    assert ex_list_3.in_('get_age_n_years_ago', [25, 30], 5) == [bob, charlie]


def test_reference_getset_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.in_(int.real, [1]) == [1]


def test_reference_method_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.in_(int.bit_length, [2]) == [2, 3]
