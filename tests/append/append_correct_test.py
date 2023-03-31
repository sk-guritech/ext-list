from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_1.append(4)

    assert ex_list_1 == [1, 2, 3, 4]

    ex_list_2 = ExList()
    ex_list_2.append(1)
    assert ex_list_2 == [1]

    ex_list_3 = ExList()
    ex_list_3.append(None)
    assert ex_list_3 == [None]
