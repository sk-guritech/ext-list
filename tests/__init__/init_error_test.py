from __future__ import annotations

import pytest

from ex_list import ExList
from tests.conftest import Person


def test_raise_type_error_by_assign_multiple_values():
    with pytest.raises(TypeError):
        ExList([1, '2'])

    with pytest.raises(TypeError):
        ExList([None, 1])

    with pytest.raises(TypeError):
        ExList([Person('alice', 25), 1])
