from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    assert ext_list_1.rename_keys({'a': 'c'}) == [{'c': 1, 'b': 2}, {'c': 3, 'b': 4}, {'c': 5, 'b': 6}]

    ext_list_2 = ExtList([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert ext_list_2.rename_keys({2: 0}) == [[3, 2], [6, 5], [9, 8]]
