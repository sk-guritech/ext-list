from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    assert ex_list_1.extract('a') == [1, 3, 5]

    ex_list_2 = ExList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    assert ex_list_2.extract('a') == [True, False, True]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ex_list_3 = ExList([alice, bob, charlie])
    assert ex_list_3.extract('name') == ['alice', 'bob', 'charlie']
    assert ex_list_3.extract('age') == [25, 30, 35]
    assert ex_list_3.extract(Person.introduce) == ['alice is 25 years old.', 'bob is 30 years old.', 'charlie is 35 years old.']
    assert ex_list_3.extract('introduce') == ['alice is 25 years old.', 'bob is 30 years old.', 'charlie is 35 years old.']
    assert ex_list_3.extract(Person.get_age_n_years_ago, 5) == [20, 25, 30]
    assert ex_list_3.extract('get_age_n_years_ago', 5) == [20, 25, 30]


def test_reference_getset_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.extract(int.real) == [1, 2, 3]


def test_reference_method_descriptor():
    ex_list_1 = ExList([1, 2, 3])

    assert ex_list_1.extract(int.bit_length) == [1, 2, 2]
