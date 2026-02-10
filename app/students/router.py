from fastapi import APIRouter, HTTPException
from typing import List
from app.students import repository, schemas

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=List[schemas.StudentResponse])
async def list_students():
    return await repository.get_all_students()

@router.post("/", response_model=schemas.StudentResponse)
async def add_student(student: schemas.StudentCreate):
    try:
        new_row = await repository.create_student(student.full_name, student.group_number)
        return dict(new_row)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Студент уже существует или данные неверны")