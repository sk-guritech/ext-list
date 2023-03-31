from __future__ import annotations

from ex_list import ExList
from tests.conftest import Person


def test():
    ex_list_1 = ExList([{'name': 'alice', 'age': 25}, {'name': 'bob', 'age': 30}, {'name': 'charlie', 'age': 35}])
    ex_list_2 = ex_list_1.dicts_to_instances(Person)

    assert len(ex_list_2) == 3
