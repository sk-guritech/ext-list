from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1}, {'a': 2}, {'a': 3}])
    assert ext_list_1.to_dict('a') == {1: {'a': 1}, 2: {'a': 2}, 3: {'a': 3}}

    ext_list_2 = ExtList([[1, 2], [3, 4], [5, 6]])
    assert ext_list_2.to_dict(0) == {1: [1, 2], 3: [3, 4], 5: [5, 6]}

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.to_dict(Person.name) == {'alice': alice, 'bob': bob, 'charlie': charlie}
    assert ext_list_3.to_dict('name') == {'alice': alice, 'bob': bob, 'charlie': charlie}
    assert ext_list_3.to_dict(Person.get_age_n_years_ago, 5) == {20: alice, 25: bob, 30: charlie}
    assert ext_list_3.to_dict('get_age_n_years_ago', 5) == {20: alice, 25: bob, 30: charlie}


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.extract(int.real) == [1, 2, 3]


def test_reference_method_descriptor():
    ext_list_4 = ExtList([1, 2, 4])
    assert ext_list_4.to_dict(int.bit_length) == {1: 1, 2: 2, 3: 4}
