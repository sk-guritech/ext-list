from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    assert ext_list_1.extract('a') == [1, 3, 5]

    ext_list_2 = ExtList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    assert ext_list_2.extract('a') == [True, False, True]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.extract('name') == ['alice', 'bob', 'charlie']
    assert ext_list_3.extract('age') == [25, 30, 35]
    assert ext_list_3.extract(Person.introduce) == ['alice is 25 years old.', 'bob is 30 years old.', 'charlie is 35 years old.']
    assert ext_list_3.extract('introduce') == ['alice is 25 years old.', 'bob is 30 years old.', 'charlie is 35 years old.']
    assert ext_list_3.extract(Person.get_age_n_years_ago, 5) == [20, 25, 30]
    assert ext_list_3.extract('get_age_n_years_ago', 5) == [20, 25, 30]


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.extract(int.real) == [1, 2, 3]


def test_reference_method_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.extract(int.bit_length) == [1, 2, 2]
