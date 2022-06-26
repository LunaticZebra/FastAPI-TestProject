def student_entity(student) -> dict:
    return {
        "student_id": int(student["student_id"]),
        "name": student["name"],
        "surname": student["surname"],
        "grades": student["grades"]
    }
def studentsEntities(entity) -> list:
    return [student_entity(item) for item in entity]