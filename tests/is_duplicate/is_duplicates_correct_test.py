from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([1, 2, 3, 3])
    ext_list_2 = ExtList([1, 2, 3, 4])
    ext_list_3 = ExtList([Person('alice', 25), Person('alice', 25)])

    bob = Person('bob', 30)
    ext_list_4 = ExtList([bob, bob])

    assert ext_list_1.is_duplicate() is True
    assert ext_list_2.is_duplicate() is False
    assert ext_list_3.is_duplicate() is False
    assert ext_list_4.is_duplicate() is True
