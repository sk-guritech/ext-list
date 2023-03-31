from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([0, 1])
    assert ex_list_1.one() == 0

    ex_list_2 = ExList([])
    assert ex_list_2.one() is None
