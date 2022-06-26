from pydantic import BaseModel
from models.Grade import Grade


class Student(BaseModel):
    student_id: int
    name: str
    surname: str
    grades: list[Grade]


class UpdateStudent(BaseModel):
    name: str
    surname: str
    grades: list[Grade]
