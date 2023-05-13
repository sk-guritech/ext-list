from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1}, {'a': 2}, {'a': 3}])

    assert ext_list_1.group_by_key('a') == {1: [{'a': 1}], 2: [{'a': 2}], 3: [{'a': 3}]}

    ext_list_2 = ExtList([[1, 2], [3, 4], [5, 6]])

    assert ext_list_2.group_by_key(0) == {1: [[1, 2]], 3: [[3, 4]], 5: [[5, 6]]}

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    david = Person(name='David', age=30)
    ext_list_3 = ExtList([alice, bob, charlie, david])

    assert ext_list_3.group_by_key('age') == {25: [alice], 30: [bob, david], 35: [charlie]}


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3, 4, 5, 6])

    assert ext_list_1.group_by_key(int.real) == {1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6]}


def test_reference_method_descriptor():
    ext_list_4 = ExtList([1, 2, 4])
    assert ext_list_4.group_by_key(int.bit_length) == {1: [1], 2: [2], 3: [4]}
