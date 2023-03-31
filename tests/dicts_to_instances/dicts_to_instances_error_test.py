from __future__ import annotations

import pytest

from ext_list import ExtList
from tests.conftest import Person


def test_raise_type_error_by_lack_of_argument():
    ext_list_1 = ExtList([{'name': 'alice'}, {'name': 'bob'}, {'name': 'charlie'}])

    with pytest.raises(TypeError):
        ext_list_1.dicts_to_instances(Person)


def test_raise_type_error_by_too_many_argument():
    ext_list_1 = ExtList([{'name': 'alice', 'age': 25, 'graduated': True}, {'name': 'bob', 'age': 30, 'graduated': True}, {'name': 'charlie', 'age': 35, 'graduated': True}])

    with pytest.raises(TypeError):
        ext_list_1.dicts_to_instances(Person)
