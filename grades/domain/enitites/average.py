from dataclasses import dataclass
import uuid


@dataclass
class Average:
    id: int
    student_id: uuid.UUID
    value: float

    def __post_init__(self):
        if self.value < 0 or self.value > 10:
            raise ValueError("Average value must be between 0 and 10")

    def __float__(self) -> float:
        return float(self.value)
