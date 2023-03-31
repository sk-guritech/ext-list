from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1}, {'a': 2}, {'a': 3}])
    assert ext_list_1.not_in_('a', [1, 2]) == [{'a': 3}]

    ext_list_2 = ExtList([{'a': True}, {'a': False}, {'a': True}])
    assert ext_list_2.not_in_('a', [True]) == [{'a': False}]

    alice = Person('alice', 25)
    bob = Person('bob', 30)
    charlie = Person('charlie', 35)

    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.not_in_(Person.age, [30, 35]) == [alice]
    assert ext_list_3.not_in_('age', [30, 35]) == [alice]
    assert ext_list_3.not_in_(Person.introduce, ['alice is 25 years old.']) == [bob, charlie]
    assert ext_list_3.not_in_('introduce', ['alice is 25 years old.']) == [bob, charlie]
    assert ext_list_3.not_in_(Person.get_age_n_years_ago, [25, 30], 5) == [alice]
    assert ext_list_3.not_in_('get_age_n_years_ago', [25, 30], 5) == [alice]


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.not_in_(int.real, [1]) == [2, 3]


def test_reference_method_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.not_in_(int.bit_length, [2]) == [1]
