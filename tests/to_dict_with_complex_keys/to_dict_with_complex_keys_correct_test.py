from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test_to_dict_with_complex_keys():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 2, 'b': 3}])

    assert ext_list_1.to_dict_with_complex_keys(['a', 'b']) == {
        (1, 2): {'a': 1, 'b': 2},
        (1, 3): {'a': 1, 'b': 3},
        (2, 3): {'a': 2, 'b': 3},
    }

    ext_list_2 = ExtList([[1, 2], [3, 4], [5, 6]])
    assert ext_list_2.to_dict_with_complex_keys([0, 1]) == {
        (1, 2): [1, 2],
        (3, 4): [3, 4],
        (5, 6): [5, 6],
    }

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.to_dict_with_complex_keys([Person.name, Person.age]) == {
        ('alice', 25): alice,
        ('bob', 30): bob,
        ('charlie', 35): charlie,
    }

    assert ext_list_3.to_dict_with_complex_keys(['name', Person.age]) == {
        ('alice', 25): alice,
        ('bob', 30): bob,
        ('charlie', 35): charlie,
    }

    assert ext_list_3.to_dict_with_complex_keys(['name', Person.introduce, Person.age]) == {
        ('alice', 'alice is 25 years old.', 25): alice,
        ('bob', 'bob is 30 years old.', 30): bob,
        ('charlie', 'charlie is 35 years old.', 35): charlie,
    }

    assert ext_list_3.to_dict_with_complex_keys(['name', 'introduce', Person.age]) == {
        ('alice', 'alice is 25 years old.', 25): alice,
        ('bob', 'bob is 30 years old.', 30): bob,
        ('charlie', 'charlie is 35 years old.', 35): charlie,
    }

    assert ext_list_3.to_dict_with_complex_keys(['name', Person.introduce, Person.get_age_n_years_ago], ((), (), (5,))) == {
        ('alice', 'alice is 25 years old.', 20): alice,
        ('bob', 'bob is 30 years old.', 25): bob,
        ('charlie', 'charlie is 35 years old.', 30): charlie,
    }

    assert ext_list_3.to_dict_with_complex_keys(['name', 'introduce', 'get_age_n_years_ago'], ((), (), (5,))) == {
        ('alice', 'alice is 25 years old.', 20): alice,
        ('bob', 'bob is 30 years old.', 25): bob,
        ('charlie', 'charlie is 35 years old.', 30): charlie,
    }
