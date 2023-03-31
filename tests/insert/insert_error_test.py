from __future__ import annotations

import pytest

from ex_list import ExList


def test_raises_type_errro_by_assign_different_type():
    ex_list_1 = ExList([1, 2, 3])

    with pytest.raises(TypeError):
        ex_list_1.insert(0, '0')
