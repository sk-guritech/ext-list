from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])
    assert ex_list_1.to_dict('a') == {1: {'a': 1}, 2: {'a': 2}, 3: {'a': 3}}

    ex_list_2 = ExList([[1, 2], [3, 4], [5, 6]])
    assert ex_list_2.to_dict(0) == {1: [1, 2], 3: [3, 4], 5: [5, 6]}

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    ex_list_3 = ExList([alice, bob, charlie])
    assert ex_list_3.to_dict(Person.name) == {'alice': alice, 'bob': bob, 'charlie': charlie}
    assert ex_list_3.to_dict('name') == {'alice': alice, 'bob': bob, 'charlie': charlie}
    assert ex_list_3.to_dict(Person.get_age_n_years_ago, 5) == {20: alice, 25: bob, 30: charlie}
    assert ex_list_3.to_dict('get_age_n_years_ago', 5) == {20: alice, 25: bob, 30: charlie}


def test_reference_getset_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.extract(int.real) == [1, 2, 3]


def test_reference_method_descriptor():
    ex_list_4 = ExList([1, 2, 4])
    assert ex_list_4.to_dict(int.bit_length) == {1: 1, 2: 2, 3: 4}
