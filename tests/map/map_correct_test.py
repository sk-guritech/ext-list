from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([1, 2, 3])
    assert ext_list_1.map(float) == [1.0, 2.0, 3.0]
