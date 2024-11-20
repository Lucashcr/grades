from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Grade:
    id: Optional[int]
    student_id: uuid.UUID
    exam: str
    value: float

    def __post_init__(self):
        if self.value < 0 or self.value > 10:
            raise ValueError("Grade value must be between 0 and 10")

    def __float__(self) -> float:
        return float(self.value)
