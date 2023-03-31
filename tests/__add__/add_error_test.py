from __future__ import annotations

import pytest

from ex_list import ExList


def test_add_raise_type_error_by_operating_between_different_types():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList(['4', '5', '6'])

    with pytest.raises(TypeError):
        ex_list_1 + ex_list_2

    with pytest.raises(TypeError):
        ex_list_2 + ex_list_1


def test_add_raise_type_error_by_add_non_exlist_object():
    ex_list_1 = ExList([1, 2, 3])
    normal_list_1 = [4, 5, 6]

    with pytest.raises(TypeError):
        ex_list_1 + normal_list_1

    with pytest.raises(TypeError):
        ex_list_1 + None

    with pytest.raises(TypeError):
        None + ex_list_1
