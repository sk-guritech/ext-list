from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([1, 2, 3])
    ext_list_2 = ExtList([4, 5, 6])

    alice = Person('Alice', 25)
    bob = Person('Bob', 30)
    charlie = Person('Charlie', 35)
    david = Person('David', 30)
    ext_list_3 = ExtList([alice, bob])
    ext_list_4 = ExtList([charlie, david])

    assert ext_list_1 + ExtList[int]([]) == [1, 2, 3]
    assert ExtList[int]([]) + ext_list_1 == [1, 2, 3]
    assert ext_list_1 + ext_list_2 == [1, 2, 3, 4, 5, 6]
    assert ext_list_3 + ext_list_4 == [alice, bob, charlie, david]


def test_right_list_and_left_ext_list():
    ext_list_1 = ExtList([1, 2, 3])
    assert [4, 5, 6] + ext_list_1 == [4, 5, 6, 1, 2, 3]
