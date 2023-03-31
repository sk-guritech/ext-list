from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    ex_list_2 = ExList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
    assert ex_list_1.extract_duplicates(ex_list_2) == [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

    ex_list_3 = ExList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    ex_list_4 = ExList([{'a': True, 'b': False}, {'a': True, 'b': True}])
    assert ex_list_3.extract_duplicates(ex_list_4) == [{'a': True, 'b': False}, {'a': True, 'b': False}]

    alice = Person(name='alice', age=25)
    alice_2 = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ex_list_5 = ExList([alice, bob, charlie])
    ex_list_6 = ExList([alice_2, bob, charlie])
    assert id(alice) != id(alice_2)
    assert ex_list_5.extract_duplicates(ex_list_6) == [bob, charlie]

    ex_list_7 = ExList([alice, bob, charlie])
    assert ex_list_5.extract_duplicates(ex_list_7) == [alice, bob, charlie]
