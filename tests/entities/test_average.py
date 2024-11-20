from uuid import uuid4

import pytest

from grades.domain.enitites.average import Average


@pytest.mark.parametrize("value", list(range(0, 11)))
def test_success_create_average_with_integer_values_between_0_and_10(value):
    student_id = uuid4()

    avg = Average(student_id, value)

    assert avg.student_id == student_id
    assert avg.value == value


@pytest.mark.parametrize("value", [value / 2 for value in range(0, 21)])
def test_success_create_average_with_float_values_between_0_and_10(value):
    student_id = uuid4()

    avg = Average(student_id, value)

    assert avg.student_id == student_id
    assert avg.value == value


def test_fail_create_average_with_value_greater_then_10():
    student_id = uuid4()
    value = 10.1

    with pytest.raises(ValueError):
        Average(student_id, value)


def test_fail_create_average_with_value_lower_then_0():
    student_id = uuid4()
    value = -0.1

    with pytest.raises(ValueError):
        Average(student_id, value)
