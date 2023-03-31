from __future__ import annotations

import pytest

from ext_list import ExtList
from tests.conftest import Person


def test_raise_type_error_by_assign_multiple_values():
    with pytest.raises(TypeError):
        ExtList([1, '2'])

    with pytest.raises(TypeError):
        ExtList([None, 1])

    with pytest.raises(TypeError):
        ExtList([Person('alice', 25), 1])
