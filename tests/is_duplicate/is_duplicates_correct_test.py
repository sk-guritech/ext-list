from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([1, 2, 3, 3])
    ex_list_2 = ExList([1, 2, 3, 4])
    ex_list_3 = ExList([Person('alice', 25), Person('alice', 25)])

    bob = Person('bob', 30)
    ex_list_4 = ExList([bob, bob])

    assert ex_list_1.is_duplicate() is True
    assert ex_list_2.is_duplicate() is False
    assert ex_list_3.is_duplicate() is False
    assert ex_list_4.is_duplicate() is True
