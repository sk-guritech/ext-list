from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test_to_dict_with_complex_keys():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 2, 'b': 3}])

    assert ex_list_1.to_dict_with_complex_keys(['a', 'b']) == {
        (1, 2): {'a': 1, 'b': 2},
        (1, 3): {'a': 1, 'b': 3},
        (2, 3): {'a': 2, 'b': 3},
    }

    ex_list_2 = ExList([[1, 2], [3, 4], [5, 6]])
    assert ex_list_2.to_dict_with_complex_keys([0, 1]) == {
        (1, 2): [1, 2],
        (3, 4): [3, 4],
        (5, 6): [5, 6],
    }

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    ex_list_3 = ExList([alice, bob, charlie])
    assert ex_list_3.to_dict_with_complex_keys([Person.name, Person.age]) == {
        ('alice', 25): alice,
        ('bob', 30): bob,
        ('charlie', 35): charlie,
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', Person.age]) == {
        ('alice', 25): alice,
        ('bob', 30): bob,
        ('charlie', 35): charlie,
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', Person.introduce, Person.age]) == {
        ('alice', 'alice is 25 years old.', 25): alice,
        ('bob', 'bob is 30 years old.', 30): bob,
        ('charlie', 'charlie is 35 years old.', 35): charlie,
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', 'introduce', Person.age]) == {
        ('alice', 'alice is 25 years old.', 25): alice,
        ('bob', 'bob is 30 years old.', 30): bob,
        ('charlie', 'charlie is 35 years old.', 35): charlie,
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', Person.introduce, Person.get_age_n_years_ago], ((), (), (5,))) == {
        ('alice', 'alice is 25 years old.', 20): alice,
        ('bob', 'bob is 30 years old.', 25): bob,
        ('charlie', 'charlie is 35 years old.', 30): charlie,
    }

    assert ex_list_3.to_dict_with_complex_keys(['name', 'introduce', 'get_age_n_years_ago'], ((), (), (5,))) == {
        ('alice', 'alice is 25 years old.', 20): alice,
        ('bob', 'bob is 30 years old.', 25): bob,
        ('charlie', 'charlie is 35 years old.', 30): charlie,
    }
