import pytest
from app.students import repository

@pytest.mark.asyncio
async def test_student_creation(db_conn, clear_db):
    student = await repository.create_student(db_conn, "Антонов А.А.", "200")
    assert student["full_name"] == "Антонов А.А."
    
    all_students = await repository.get_all_students(db_conn)
    assert len(all_students) == 1

@pytest.mark.asyncio
async def test_student_uniqueness(db_conn):
    await repository.create_student(db_conn, "Иванов", "101")
    with pytest.raises(Exception): # Нарушение UNIQUE constraint
        await repository.create_student(db_conn, "Иванов", "101")