from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'name': 'alice', 'age': 25}, {'name': 'bob', 'age': 30}, {'name': 'charlie', 'age': 35}])
    ext_list_2 = ext_list_1.dicts_to_instances(Person)

    assert len(ext_list_2) == 3
