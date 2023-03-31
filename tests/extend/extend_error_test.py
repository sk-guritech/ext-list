from __future__ import annotations

import pytest

from ext_list import ExtList


def test_raises_type_error_by_assign_invalid_object():
    ext_list_1 = ExtList([1, 2, 3])
    normal_list_1 = [4]

    with pytest.raises(TypeError):
        ext_list_1.append(normal_list_1)


def test_raises_type_error_by_assign_different_type():
    ext_list_1 = ExtList([1, 2, 3])
    ext_list_2 = ExtList(['4', '5', '6'])

    with pytest.raises(TypeError):
        ext_list_1.append(ext_list_2)
