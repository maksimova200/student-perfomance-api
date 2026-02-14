from asyncpg import Connection
from typing import List, Dict

async def get_all_students(conn: Connection) -> List[Dict]:
    """Возвращает список всех студентов из БД."""
    rows = await conn.fetch("SELECT id, full_name, group_number FROM students")
    return [dict(row) for row in rows]

async def create_student(conn: Connection, full_name: str, group_number: str) -> Dict:
    """Создает нового студента в БД."""

    return await conn.fetchrow(
        "INSERT INTO students (full_name, group_number) VALUES ($1, $2) RETURNING id, full_name, group_number",
        full_name, group_number
    )
    
async def get_students_by_more_twos(conn: Connection, count: int) -> List[Dict]:
    """Возвращает студентов, у которых количество двоек больше указанного."""
    query = f"""
        SELECT s.full_name, COUNT(g.id)::int as count_twos
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE g.grade = 2
        GROUP BY s.id, s.full_name
        HAVING COUNT(g.id) > $1
        ORDER BY count_twos DESC
    """
    rows = await conn.fetch(query, count)
    return [dict(row) for row in rows]

async def get_students_by_less_twos(conn: Connection, count: int) -> List[Dict]:
    """Возвращает студентов, у которых количество двоек меньше указанного."""
    query = f"""
        SELECT s.full_name, COUNT(g.id)::int as count_twos
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE g.grade = 2
        GROUP BY s.id, s.full_name
        HAVING COUNT(g.id) < $1
        ORDER BY count_twos DESC
    """
    rows = await conn.fetch(query, count)
    return [dict(row) for row in rows]