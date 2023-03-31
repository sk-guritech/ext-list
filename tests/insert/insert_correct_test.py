from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([1, 2, 3])

    ex_list_1.insert(0, 0)
    assert ex_list_1 == [0, 1, 2, 3]
