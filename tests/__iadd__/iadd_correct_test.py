from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList([4, 5, 6])

    ex_list_1 += ex_list_2

    assert ex_list_1 == [1, 2, 3, 4, 5, 6]
    assert ex_list_2 == [4, 5, 6]
