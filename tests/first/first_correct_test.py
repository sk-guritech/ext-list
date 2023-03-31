from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([0, 1])

    assert ex_list_1.first() == 0
