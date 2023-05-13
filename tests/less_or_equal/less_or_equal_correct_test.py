from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}])

    assert ext_list_1.less_or_equal('age', 30) == [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    david = Person(name='David', age=30)
    ext_list_2 = ExtList([alice, bob, charlie, david])

    assert ext_list_2.less_or_equal(Person.age, 30) == [alice, bob, david]
    assert ext_list_2.less_or_equal(Person.get_age_n_years_ago, 25, 5) == [alice, bob, david]


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.less_or_equal(int.real, 2) == [1, 2]


def test_reference_method_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.less_or_equal(int.bit_length, 2) == [1, 2, 3]
