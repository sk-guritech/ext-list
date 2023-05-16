import pytest

from ext_list import ExtList


def test_raise_type_error_by_non_indexable_object():
    ext_list = ExtList([1, 2, 3])

    with pytest.raises(TypeError):
        ext_list.map_for_keys(['a'], str)
