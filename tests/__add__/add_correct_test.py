from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([4, 5, 6])

    alice = Person('Alice', 25)
    bob = Person('Bob', 30)
    charlie = Person('Charlie', 35)
    david = Person('David', 30)
    ex_list_3 = ExList([alice, bob])
    ex_list_4 = ExList([charlie, david])

    assert ex_list_1 + ExList[int]([]) == [1, 2, 3]
    assert ExList[int]([]) + ex_list_1 == [1, 2, 3]
    assert ex_list_1 + ex_list_2 == [1, 2, 3, 4, 5, 6]
    assert ex_list_3 + ex_list_4 == [alice, bob, charlie, david]


def test_right_list_and_left_ex_list():
    ex_list_1 = ExList([1, 2, 3])
    assert [4, 5, 6] + ex_list_1 == [4, 5, 6, 1, 2, 3]
