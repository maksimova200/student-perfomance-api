import os
import asyncpg
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(dsn=DATABASE_URL)
            print("Подключение к пулу БД установлено")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            print("Пул БД закрыт")

database = Database()