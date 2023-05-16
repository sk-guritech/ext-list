from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list = ExtList([{'name': 'alice', 'age': 25}, {'name': 'bob', 'age': 30}])
    assert ext_list.map_for_keys(['name'], str.capitalize) == [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
