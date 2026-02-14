from fastapi import APIRouter, HTTPException, Depends
from asyncpg import Connection
from typing import List
from app.students import repository, schemas
from app.database import get_connection

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=List[schemas.StudentResponse])
async def list_students(conn: Connection = Depends(get_connection)):
    """Возвращает список всех студентов."""
    return await repository.get_all_students(conn)

@router.post("/", response_model=schemas.StudentResponse)
async def add_student(
    student: schemas.StudentCreate,
    conn: Connection = Depends(get_connection)
):
    """Создает нового студента."""
    try:
        new_row = await repository.create_student(conn, student.full_name, student.group_number)
        return dict(new_row)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Студент уже существует или данные неверны")
    
@router.get("/more-than-3-twos", response_model=List[schemas.StudentAnalytics])
async def get_more_than_3_twos(conn: Connection = Depends(get_connection)):
    """Список студентов, у которых более 3 двоек"""
    return await repository.get_students_by_more_twos(conn, 3)

@router.get("/less-than-5-twos", response_model=List[schemas.StudentAnalytics])
async def get_students_by_less_twos(conn: Connection = Depends(get_connection)):
    """Список студентов, у которых менее 5 двоек"""
    return await repository.get_students_by_less_twos(conn, 5)