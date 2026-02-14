from typing import List, Dict
from asyncpg import Connection
from app.grades.schemas import GradeCSVRow

def build_grades_data(rows: List[GradeCSVRow], student_map: Dict[tuple, int]) -> List[tuple]:
    """Строит список кортежей с данными для вставки оценок в базу данных."""
    grades_data = []

    for row in rows:
        key = (row.full_name, row.group_number)
        student_id = student_map.get(key)

        if student_id:
            grades_data.append(
                (student_id, row.grade, row.lesson_date)
            )

    return grades_data

async def upsert_students(rows: List[GradeCSVRow], conn: Connection) -> Dict[tuple, int]:
    """ Вставляет уникальных студентов в базу данных и возвращает маппинг их ID."""
    unique_students = list({(r.full_name, r.group_number) for r in rows})

    await conn.executemany(
        """
        INSERT INTO students (full_name, group_number)
        VALUES ($1, $2)
        ON CONFLICT (full_name, group_number) DO NOTHING
        """,
        unique_students
    )

    names = [s[0] for s in unique_students]
    groups = [s[1] for s in unique_students]

    db_students = await conn.fetch("""
        SELECT s.id, s.full_name, s.group_number 
        FROM students s
        JOIN unnest($1::text[], $2::text[]) AS input(name, group_num)
        ON s.full_name = input.name 
        AND s.group_number = input.group_num
    """, names, groups)

    return {
        (r["full_name"], r["group_number"]): r["id"]
        for r in db_students
    }

async def bulk_insert_grades(rows: List[GradeCSVRow], conn: Connection) -> Dict[str, int]:
    """Выполняет массовую вставку оценок в базу данных"""
    async with conn.transaction():

        student_map = await upsert_students(rows, conn)

        grades_data = build_grades_data(rows, student_map)

        await conn.executemany(
            """
            INSERT INTO grades (student_id, grade, lesson_date)
            VALUES ($1, $2, $3)
            """,
            grades_data
        )

        return {
            "records_loaded": len(rows),
            "students": len(student_map),
        }