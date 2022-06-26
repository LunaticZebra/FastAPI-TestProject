from pydantic import BaseModel
from enum import Enum


class Course(str, Enum):
    pe = "PE"
    chemistry = "chemistry"
    biology = "biology"
    physics = "physics"
    math = "math"
    history = "history"


def possible_grades() -> list[float]:
    return [1, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]


class Grade(BaseModel):
    grade: float
    course: Course
    weight: int

    def check_grade(self):
        return self.grade in possible_grades()
