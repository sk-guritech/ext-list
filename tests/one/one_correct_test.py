from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([0, 1])
    assert ext_list_1.one() == 0

    ext_list_2 = ExtList([])
    assert ext_list_2.one() is None
