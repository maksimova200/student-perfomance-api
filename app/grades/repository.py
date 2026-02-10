from typing import List, Dict
from app.database import database
from app.grades.schemas import GradeCSVRow

async def bulk_insert_grades(rows: List[GradeCSVRow]) -> Dict[str, int]:
    async with database.pool.acquire() as conn:
        async with conn.transaction():
            # Собираем уникальных студентов
            students = {
                (row.full_name, row.group_number)
                for row in rows
            }

            await conn.executemany(
                """
                INSERT INTO students (full_name, group_number)
                VALUES ($1, $2)
                ON CONFLICT (full_name, group_number) DO NOTHING
                """,
                list(students)
            )

            # Маппим 
            names = [name for name, group in students]
            groups = [group for name, group in students]
            
            db_students = await conn.fetch("""
                SELECT s.id, s.full_name, s.group_number 
                FROM students s
                JOIN unnest($1::text[], $2::text[]) AS input(name, group_num)
                ON s.full_name = input.name AND s.group_number = input.group_num
            """, names, groups)
            
            student_map = {
                (r["full_name"], r["group_number"]): r["id"] 
                for r in db_students
            }

            # Готовим для вставки 
            grades_data = [
                (
                    student_map[(row.full_name, row.group_number)],
                    row.grade,
                    row.lesson_date
                )
                for row in rows
            ]

            await conn.executemany(
                """
                INSERT INTO grades (student_id, grade, lesson_date)
                VALUES ($1, $2, $3)
                """,
                grades_data
            )

            return {
                "records_loaded": len(rows),
                "new_students_potential": len(students)
            }