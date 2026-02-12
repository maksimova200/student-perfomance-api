from app.database import database

async def get_all_students():
    async with database.pool.acquire() as connection:
        rows = await connection.fetch("SELECT id, full_name, group_number FROM students")
        return [dict(row) for row in rows]

async def create_student(full_name: str, group_number: str):
    async with database.pool.acquire() as connection:
        return await connection.fetchrow(
            "INSERT INTO students (full_name, group_number) VALUES ($1, $2) RETURNING id, full_name, group_number",
            full_name, group_number
        )
    
async def get_students_by_twos_limit(operator: str, count: int):
    query = f"""
        SELECT s.full_name, COUNT(g.id)::int as count_twos
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE g.grade = 2
        GROUP BY s.id, s.full_name
        HAVING COUNT(g.id) {operator} $1
        ORDER BY count_twos DESC
    """
    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query, count)
        return [dict(row) for row in rows]