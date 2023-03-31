from __future__ import annotations

import pytest

from ext_list import ExtList


def test_raise_index_error_by_reference_empty_ext_list():
    ext_list_1 = ExtList()
    with pytest.raises(IndexError):
        ext_list_1[0]
