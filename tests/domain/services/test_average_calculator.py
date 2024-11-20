import pytest
import uuid

from grades.domain.enitites.average import Average
from grades.domain.services.average_calculator import (
    AverageCalculator,
    MeanAverageStrategy,
    WeightedAverageStrategy,
)
from grades.domain.enitites.grade import Grade


def test_success_calculate_mean_without_weights():
    student_id = uuid.uuid4()
    grades = [
        Grade(None, student_id, "P1", 10),
        Grade(None, student_id, "P2", 9),
        Grade(None, student_id, "P3", 5),
    ]

    strategy = MeanAverageStrategy()
    calculator = AverageCalculator(strategy)
    average = calculator.execute(grades)

    assert average == Average(None, student_id, 8)


def test_success_calculate_mean_with_weights():
    student_id = uuid.uuid4()
    grades = [
        Grade(None, student_id, "P1", 10),
        Grade(None, student_id, "P2", 9),
        Grade(None, student_id, "P3", 5),
    ]

    weights = [3.0, 3.0, 4.0]

    strategy = WeightedAverageStrategy()
    calculator = AverageCalculator(strategy)
    average = calculator.execute(grades, weights)

    assert average == Average(None, student_id, 7.7)


def test_fail_calculate_average_with_empty_grades_sequence():
    grades = []

    with pytest.raises(ValueError):
        MeanAverageStrategy.execute(grades)
