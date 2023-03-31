from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([0, 1])

    assert ext_list_1.first() == 0
