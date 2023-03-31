from __future__ import annotations

import pytest

from ex_list import ExList


def test_raises_type_error_by_assign_invalid_object():
    ex_list_1 = ExList([1, 2, 3])
    normal_list_1 = [4]

    with pytest.raises(TypeError):
        ex_list_1.append(normal_list_1)


def test_raises_type_error_by_assign_different_type():
    ex_list_1 = ExList([1, 2, 3])
    ex_list_2 = ExList(['4', '5', '6'])

    with pytest.raises(TypeError):
        ex_list_1.append(ex_list_2)
