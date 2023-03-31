from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([1, 2, 3])

    ext_list_1.insert(0, 0)
    assert ext_list_1 == [0, 1, 2, 3]
