from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    assert ExList([1, 2, 3]) == [1, 2, 3]

    assert ExList(['1', '2', '3']) == ['1', '2', '3']

    assert ExList([[1, 2], [3, 4], [5, 6]]) == [[1, 2], [3, 4], [5, 6]]

    assert ExList([{'k': 1}, {'k': 2}, {'k': 3}]) == [{'k': 1}, {'k': 2}, {'k': 3}]

    alice = Person('alice', 25)
    bob = Person('bob', 30)
    assert ExList([alice, bob]) == [alice, bob]

    assert ExList() == []
