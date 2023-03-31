from __future__ import annotations

import pytest

from ext_list import ExtList


def test_add_raise_type_error_by_operating_between_different_types():
    ext_list_1 = ExtList([1, 2, 3])
    ext_list_2 = ExtList(['4', '5', '6'])

    with pytest.raises(TypeError):
        ext_list_1 + ext_list_2

    with pytest.raises(TypeError):
        ext_list_2 + ext_list_1


def test_add_raise_type_error_by_add_non_ExtList_object():
    ext_list_1 = ExtList([1, 2, 3])
    normal_list_1 = [4, 5, 6]

    with pytest.raises(TypeError):
        ext_list_1 + normal_list_1

    with pytest.raises(TypeError):
        ext_list_1 + None

    with pytest.raises(TypeError):
        None + ext_list_1
