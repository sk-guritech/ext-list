from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    ext_list_2 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
    assert ext_list_1.extract_duplicates(ext_list_2) == [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

    ext_list_3 = ExtList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    ext_list_4 = ExtList([{'a': True, 'b': False}, {'a': True, 'b': True}])
    assert ext_list_3.extract_duplicates(ext_list_4) == [{'a': True, 'b': False}, {'a': True, 'b': False}]

    alice = Person(name='alice', age=25)
    alice_2 = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ext_list_5 = ExtList([alice, bob, charlie])
    ext_list_6 = ExtList([alice_2, bob, charlie])
    assert id(alice) != id(alice_2)
    assert ext_list_5.extract_duplicates(ext_list_6) == [bob, charlie]

    ext_list_7 = ExtList([alice, bob, charlie])
    assert ext_list_5.extract_duplicates(ext_list_7) == [alice, bob, charlie]
