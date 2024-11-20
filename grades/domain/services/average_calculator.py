from abc import ABC, abstractmethod
from typing import Optional

from grades.domain.enitites.grade import Grade
from grades.domain.enitites.average import Average


class AverageStrategy(ABC):
    @staticmethod
    @abstractmethod
    def execute(grades: list[Grade], weights: Optional[list[float]]) -> Average: ...


class MeanAverageStrategy(AverageStrategy):
    @staticmethod
    def execute(grades: list[Grade], weights: Optional[list[float]] = None) -> Average:
        if not grades:
            raise ValueError("Grades list must not be empty")

        current_student_id = grades[0].student_id

        total = 0.0
        for grade in grades:
            total += grade.value

        avg = total / len(grades)
        return Average(None, current_student_id, avg)


class WeightedAverageStrategy(AverageStrategy):
    @staticmethod
    def execute(grades: list[Grade], weights: Optional[list[float]]) -> Average:
        if not grades:
            raise ValueError("Grades list must not be empty")

        if not weights:
            raise ValueError("Weights list must not be empty")

        current_student_id = grades[0].student_id

        total = 0.0
        for grade, weight in zip(grades, weights):
            total += grade.value * weight

        avg = total / sum(weights)
        return Average(None, current_student_id, avg)


class AverageCalculator:
    def __init__(self, strategy: AverageStrategy) -> None:
        self.strategy = strategy

    def execute(self, grades: list[Grade], weights: Optional[list[float]] = None):
        return self.strategy.execute(grades, weights)
