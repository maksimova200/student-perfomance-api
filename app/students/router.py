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
    
@router.get("/more-than-3-twos", response_model=List[schemas.StudentAnalytics])
async def get_more_than_3_twos():
    """Список студентов, у которых более 3 двоек"""
    return await repository.get_students_by_twos_limit(">", 3)

@router.get("/less-than-5-twos", response_model=List[schemas.StudentAnalytics])
async def get_less_than_5_twos():
    """Список студентов, у которых менее 5 двоек"""
    return await repository.get_students_by_twos_limit("<", 5)