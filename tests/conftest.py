import pytest
import os
import asyncpg
os.environ["DATABASE_URL"] = "postgresql://my_secure_user:my_super_secret_password@db:5432/students_db"

from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_connection


@pytest.fixture(scope="function")
async def pool():
    """Создаем пул для тестов"""
    pool = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    yield pool
    await pool.close()

@pytest.fixture(autouse=False)
async def clear_db(pool):
    """Очистка перед каждым тестом"""
    async with pool.acquire() as conn:
        await conn.execute("TRUNCATE students, grades RESTART IDENTITY CASCADE;")

@pytest.fixture
async def client(pool):
    """Клиент с подменой зависимости"""
    app.state.pool = pool
    
    async def override_get_connection():
        async with pool.acquire() as conn:
            yield conn
    
    app.dependency_overrides[get_connection] = override_get_connection
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
async def db_conn(pool):
    """Предоставляет соединение из пула для каждого теста."""
    async with pool.acquire() as conn:
        yield conn

@pytest.fixture
def csv_factory():
    """Фабрика CSV"""
    def _make_csv(rows: list):
        header = "Дата;Номер группы;ФИО;Оценка"
        return header + "\n" + "\n".join(rows)
    return _make_csv