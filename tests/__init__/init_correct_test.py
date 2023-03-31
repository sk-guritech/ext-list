from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    assert ExtList([1, 2, 3]) == [1, 2, 3]

    assert ExtList(['1', '2', '3']) == ['1', '2', '3']

    assert ExtList([[1, 2], [3, 4], [5, 6]]) == [[1, 2], [3, 4], [5, 6]]

    assert ExtList([{'k': 1}, {'k': 2}, {'k': 3}]) == [{'k': 1}, {'k': 2}, {'k': 3}]

    alice = Person('alice', 25)
    bob = Person('bob', 30)
    assert ExtList([alice, bob]) == [alice, bob]

    assert ExtList() == []
