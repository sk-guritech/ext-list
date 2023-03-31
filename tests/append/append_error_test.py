from __future__ import annotations

import pytest

from ext_list import ExtList


def test_raises_type_error_by_assign_different_type():
    ext_list_1 = ExtList([1, 2, 3])

    with pytest.raises(TypeError):
        ext_list_1.append('4')

    with pytest.raises(TypeError):
        ext_list_1.append(None)

    with pytest.raises(TypeError):
        ext_list_1.append([])
