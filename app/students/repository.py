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