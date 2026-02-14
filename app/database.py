from fastapi import Request
import asyncpg
from typing import AsyncGenerator

async def get_connection(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    """Зависимость FastAPI для получения соединения с БД из пула."""
    async with request.app.state.pool.acquire() as conn:
        yield conn