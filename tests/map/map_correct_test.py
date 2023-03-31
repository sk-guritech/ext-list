from __future__ import annotations

from ex_list import ExList


def test():
    ex_list_1 = ExList([1, 2, 3])
    assert ex_list_1.map(float) == [1.0, 2.0, 3.0]
