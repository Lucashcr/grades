from abc import ABC, abstractmethod

from grades.domain.enitites.grade import Grade
from grades.domain.enitites.average import Average


class AverageCalculator(ABC):
    @staticmethod
    @abstractmethod
    def execute(grades: list[Grade]) -> Average: ...


class MeanAverageCalculator(AverageCalculator):
    @staticmethod
    def execute(grades: list[Grade], weights: list[float] = []) -> Average:
        if len(grades) == 0:
            raise ValueError("Grades list must not be empty")

        current_student_id = grades[0].student_id

        total = 0.0
        for grade in grades:
            total += grade.value

        avg = total / len(grades)
        return Average(current_student_id, avg)
