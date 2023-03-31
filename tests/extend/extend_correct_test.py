from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([4, 5, 6])
    ex_list_3 = ExList[int]([])
    ex_list_4 = ExList[None]([])
    ex_list_5 = ExList([None])

    ex_list_1.extend(ex_list_2)
    assert ex_list_1 == [1, 2, 3, 4, 5, 6]

    ex_list_2.extend(ex_list_3)
    assert ex_list_2 == [4, 5, 6]

    ex_list_4.extend(ex_list_5)
    assert ex_list_4 == [None]
