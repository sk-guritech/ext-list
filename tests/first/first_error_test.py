from __future__ import annotations

import pytest

from ex_list import ExList


def test_raise_index_error_by_reference_empty_ex_list():
    ex_list_1 = ExList()
    with pytest.raises(IndexError):
        ex_list_1[0]
