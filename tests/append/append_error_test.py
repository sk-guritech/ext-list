from __future__ import annotations

import pytest

from ex_list import ExList


def test_raises_type_error_by_assign_different_type():
    ex_list_1 = ExList([1, 2, 3])

    with pytest.raises(TypeError):
        ex_list_1.append('4')

    with pytest.raises(TypeError):
        ex_list_1.append(None)

    with pytest.raises(TypeError):
        ex_list_1.append([])
