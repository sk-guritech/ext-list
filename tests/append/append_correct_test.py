from __future__ import annotations

from ext_list import ExtList


def test():
    ext_list_1 = ExtList([1, 2, 3])
    ext_list_1.append(4)

    assert ext_list_1 == [1, 2, 3, 4]

    ext_list_2 = ExtList()
    ext_list_2.append(1)  # type: ignore
    assert ext_list_2 == [1]

    ext_list_3 = ExtList()
    ext_list_3.append(None)  # type: ignore
    assert ext_list_3 == [None]
