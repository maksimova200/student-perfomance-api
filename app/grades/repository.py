from typing import List, Dict
from asyncpg import Connection
from app.grades.schemas import GradeCSVRow

async def bulk_insert_grades(rows: List[GradeCSVRow], conn: Connection) -> Dict[str, int]:
    async with conn.transaction():
        unique_students = list({(row.full_name, row.group_number) for row in rows})

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
        
        student_map = {
            (r["full_name"], r["group_number"]): r["id"] 
            for r in db_students
        }

        grades_data = []
        for row in rows:
            key = (row.full_name, row.group_number)
            student_id = student_map.get(key)
            if student_id:
                grades_data.append((student_id, row.grade, row.lesson_date))

        await conn.executemany(
            """
            INSERT INTO grades (student_id, grade, lesson_date)
            VALUES ($1, $2, $3)
            """,
            grades_data
        )

        return {
            "in_file": len(rows),
            "in_db": len(grades_data),
            "map_size": len(student_map)
        }