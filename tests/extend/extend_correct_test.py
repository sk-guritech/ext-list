from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([1, 2, 3])
    ext_list_2 = ExtList([4, 5, 6])
    ext_list_3 = ExtList[int]([])
    ext_list_4 = ExtList[None]([])
    ext_list_5 = ExtList([None])

    ext_list_1.extend(ext_list_2)
    assert ext_list_1 == [1, 2, 3, 4, 5, 6]

    ext_list_2.extend(ext_list_3)
    assert ext_list_2 == [4, 5, 6]

    ext_list_4.extend(ext_list_5)
    assert ext_list_4 == [None]
