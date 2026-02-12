import pytest
import asyncio
import os
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import database

# Переключаем приложение на тестовую БД
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/student_db_test"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def db_setup():
    await database.connect()
    yield
    await database.disconnect()

@pytest.fixture(autouse=True)
async def clear_db():
    # Очистка таблиц перед каждым тестом
    async with database.pool.acquire() as conn:
        await conn.execute("TRUNCATE students, grades RESTART IDENTITY CASCADE;")
    yield

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# Фабрика для CSV строк
@pytest.fixture
def csv_factory():
    def _make_csv(rows: list):
        header = "Дата;Номер группы;ФИО;Оценка"
        return header + "\n" + "\n".join(rows)
    return _make_csv