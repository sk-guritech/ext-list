from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1}, {'a': 2}, {'a': 3}])
    assert ext_list_1.in_('a', [1, 2]) == [{'a': 1}, {'a': 2}]

    ext_list_2 = ExtList([{'a': True}, {'a': False}, {'a': True}])
    assert ext_list_2.in_('a', [True]) == [{'a': True}, {'a': True}]

    alice = Person('alice', 25)
    bob = Person('bob', 30)
    charlie = Person('charlie', 35)

    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.in_(Person.age, [30, 35]) == [bob, charlie]
    assert ext_list_3.in_('age', [30, 35]) == [bob, charlie]
    assert ext_list_3.in_(Person.introduce, ['alice is 25 years old.']) == [alice]
    assert ext_list_3.in_('introduce', ['alice is 25 years old.']) == [alice]
    assert ext_list_3.in_(Person.get_age_n_years_ago, [25, 30], 5) == [bob, charlie]
    assert ext_list_3.in_('get_age_n_years_ago', [25, 30], 5) == [bob, charlie]


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.in_(int.real, [1]) == [1]


def test_reference_method_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.in_(int.bit_length, [2]) == [2, 3]
