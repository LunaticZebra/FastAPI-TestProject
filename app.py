from fastapi import FastAPI, status, HTTPException, Path
from models.Grade import Grade, possible_grades
from models.Student import Student, UpdateStudent
from pymongo import errors
from pprint import pprint
from schemas.student_schema import studentsEntities
from database.mongo_db import MyDatabase

app = FastAPI()
database = MyDatabase()
students = database.students

# tworzymy studenta
@app.post("/students/", status_code=status.HTTP_201_CREATED)
async def create_student(new_student: Student):
    try:
        students.insert_one(new_student.dict())
        pprint(new_student)
        return new_student
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Item already exists")


# aktualizujemy studenta wyszukując go po id
@app.put("/student")
async def update_student(student_id: int, student_update: UpdateStudent):
    retrieved_data = students.find_one({"student_id": student_id})
    if retrieved_data:
        old_student = Student(**retrieved_data)
        updated_student = old_student.copy(update=student_update.dict())
        students.replace_one({"student_id": student_id}, updated_student.dict())
        return student_update

    else:
        raise status.HTTP_404_NOT_FOUND


# aktualizujemy oceny studenta, wyszukując go po id
@app.put("/student/{student_id}/grades", status_code=status.HTTP_202_ACCEPTED, response_model=Student)
async def add_grade(*, student_id: int = Path(title="The ID of the student"), new_grade: Grade):
    if new_grade.check_grade():
        student = students.find_one({"student_id": student_id})
        grades = student["grades"]
        grades.append(new_grade.dict())
        pprint(grades)
        students.update_one({"student_id": student_id}, {"$set": {'grades': grades}})
        return student
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong grade, possible grades - " +
              str(possible_grades()).strip("[]"))


# pobieramy dane wszystkich studentów
@app.get("/students")
async def get_students():
    return studentsEntities(students.find())


# szukamy studenta o podanym id
@app.get("/students/{student_id}", response_model=Student)
async def get_student_id(student_id: int = Path(title="The ID of the student")):
    student = students.find_one({"student_id": student_id})
    if student:
        return student
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


# usuwamy studenta o podanym id
@app.delete("/student/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int = Path(title="The ID of the student")):
    if students.delete_one({"student_id": student_id}).deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")