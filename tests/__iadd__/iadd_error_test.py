from __future__ import annotations

import pytest

from ext_list import ExtList


def test_raise_type_error_by_assign_non_ExtList_object():
    ext_list_1 = ExtList([1, 2, 3])
    normal_list_1 = [4, 5, 6]

    with pytest.raises(TypeError):
        ext_list_1 += normal_list_1
