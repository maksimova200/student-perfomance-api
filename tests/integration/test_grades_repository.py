import pytest
from app.grades.repository import bulk_insert_grades
from app.grades.schemas import GradeCSVRow
from datetime import date

@pytest.mark.asyncio
async def test_bulk_insert_and_unnest_logic(db_conn):
    rows = [
        GradeCSVRow(lesson_date=date(2025,1,1), group_number="101", full_name="Сидоров", grade=2),
        GradeCSVRow(lesson_date=date(2025,1,2), group_number="101", full_name="Сидоров", grade=3),
    ]
    result = await bulk_insert_grades(rows, db_conn)
    
    assert result["records_loaded"] == 2
    assert result["students"] == 1 # Должен создаться 1 студент на 2 оценки