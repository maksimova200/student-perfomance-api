import os
import asyncpg
import logging
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL")

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(dsn=DATABASE_URL)
            logger.info("Подключение к пулу БД установлено")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("Пул БД закрыт")

database = Database()