# type: ignore
from __future__ import annotations

from ext_list import ExtList


class A:
    def __init__(self, value: int):
        self.__value = value % 700

    @property
    def value(self) -> str:
        return self.__value


def equal_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value == 300]

    def use_ext_list(targets: ExtList[A]):
        return targets.equal(A.value, 300)

    list_comprehension(targets)
    use_ext_list(targets)


def not_equal_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value != 300]

    def use_ext_list(targets: ExtList[A]):
        return targets.not_equal(A.value, 300)

    list_comprehension(targets)
    use_ext_list(targets)


def greater_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value > 300]

    def use_ext_list(targets: ExtList[A]):
        return targets.greater(A.value, 300)

    list_comprehension(targets)
    use_ext_list(targets)


def greater_or_equal_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value >= 300]

    def use_ext_list(targets: ExtList[A]):
        return targets.greater_or_equal(A.value, 300)

    list_comprehension(targets)
    use_ext_list(targets)


def less_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value < 300]

    def use_ext_list(targets: ExtList[A]):
        return targets.greater(A.value, 300)

    list_comprehension(targets)
    use_ext_list(targets)


def less_or_equal_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value <= 300]

    def use_ext_list(targets: ExtList[A]):
        return targets.greater_or_equal(A.value, 300)

    list_comprehension(targets)
    use_ext_list(targets)


def in_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value in [100, 200, 300, 400, 500, 600, 700]]

    def use_ext_list(targets: ExtList[A]):
        return targets.in_(A.value, [100, 200, 300, 400, 500, 600, 700])

    list_comprehension(targets)
    use_ext_list(targets)


def not_in_test(targets: ExtList[A]):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target.value not in [100, 200, 300, 400, 500, 600, 700]]

    def use_ext_list(targets: ExtList[A]):
        return targets.not_in_(A.value, [100, 200, 300, 400, 500, 600, 700])

    list_comprehension(targets)
    use_ext_list(targets)


def extract_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target.value for target in targets]

    def use_ext_list(targets: ExtList[A]):
        return targets.extract(A.value)

    list_comprehension(targets)
    use_ext_list(targets)


def extract_duplicates_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target for target in targets if target in [100, 200, 300, 400, 500, 600, 700, -1, -2]]

    def use_ext_list(targets: ExtList[A]):
        return targets.extract_duplicates([100, 200, 300, 400, 500, 600, 700, -1, -2])

    list_comprehension(targets)
    use_ext_list(targets)


def is_duplicate_test(targets):
    def list_comprehension(targets):
        return (len(targets) - len(set(targets))) > 0

    def use_ext_list(targets):
        return targets.is_duplicate()

    list_comprehension(targets)
    use_ext_list(targets)


def map_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [float(target) for target in targets]

    def use_ext_list(targets: ExtList[A]):
        return targets.map(float)

    list_comprehension(targets)
    use_ext_list(targets)


def to_dict_test(targets):
    def list_comprehension(targets: ExtList[A]):
        return [target.value for target in targets]

    def use_ext_list(targets: ExtList[A]):
        return targets.to_dict(A.value)

    list_comprehension(targets)
    use_ext_list(targets)


def dicts_to_instances_test(dict_targets):
    def list_comprehension(dict_targets):
        return [A(**target) for target in dict_targets]

    def use_ext_list(dict_targets):
        return dict_targets.dicts_to_instances(A)

    list_comprehension(dict_targets)
    use_ext_list(dict_targets)


def rename_keys_test(dict_targets):
    def list_comprehension(dict_targets):
        return [{'Value': target['value']} for target in dict_targets]

    def use_ext_list(dict_targets):
        return dict_targets.rename_keys({'value': 'Value'})

    list_comprehension(dict_targets)
    use_ext_list(dict_targets)


def group_by_key_test(int_targets):
    def use_ext_list(int_targets):
        return int_targets.group_by_key(int.bit_length)

    use_ext_list(int_targets)


def map_for_keys_test(dict_targets):
    def list_comprehension(dict_targets):
        return [int.bit_length(target['value']) for target in dict_targets]

    def use_ext_list(dict_targets):
        return dict_targets.map_for_keys(['value'], int.bit_length)

    list_comprehension(dict_targets)
    use_ext_list(dict_targets)


def to_dict_list_test(dict_targets):
    def list_comprehension(dict_targets):
        return [{'value': target['value']} for target in dict_targets]

    def use_ext_list(dict_targets):
        return dict_targets.to_dict_list(['value'])

    list_comprehension(dict_targets)
    use_ext_list(dict_targets)


def to_dict_with_complex_keys_test(dict_targets):
    def list_comprehension(dict_targets):
        return {(target['value'], target['name']): target for target in dict_targets}

    def use_ext_list(dict_targets):
        return dict_targets.to_dict_with_complex_keys(['value', 'name'])

    list_comprehension(dict_targets)
    use_ext_list(dict_targets)


if __name__ == '__main__':
    ELEMENT_LENGTH = 2000000
    targets = ExtList([A(i) for i in range(ELEMENT_LENGTH)])
    int_targets = ExtList([i for i in range(ELEMENT_LENGTH)])
    dict_targets = ExtList([{'value': i, 'name': i + 1} for i in range(ELEMENT_LENGTH)])

    # OperatorOperations  use_ext_list / list-comprehension
    equal_test(targets)  # 0.517 / 0.359
    not_equal_test(targets)  # 0.548 / 0.381
    greater_test(targets)  # 0.526 / 0.372
    greater_or_equal_test(targets)  # 0.528 / 0.374
    less_test(targets)  # 0.532 / 0.377
    less_or_equal_test(targets)  # 0.528 / 0.372
    in_test(targets)  # 0.624 / 0.426
    not_in_test(targets)  # 0.659 / 0.447

    # ListOperations
    extract_test(targets)  # 0.502 / 0.353
    extract_duplicates_test(int_targets)  # 0.204 / 0.134
    is_duplicate_test(targets)  # 0.0549 / 0.0598
    map_test(int_targets)  # 0.247 / 0.111

    # DictOperations
    to_dict_test(targets)  # 0.512 / 0.345
    # to_dict_list_test(dict_targets)  # 1.25 / 0.264
    dicts_to_instances_test(dict_targets)  # 1.29 / 1.30
    group_by_key_test(int_targets)  # 1.20 / NA
    rename_keys_test(dict_targets)  # 1.16 / 0.269
    # map_for_keys_test(dict_targets)  # 11.4 / 0.382
    # to_dict_with_complex_keys_test(dict_targets)  # 2.09 / 0.442
