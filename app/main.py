from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import os
import asyncpg
from app.students.router import router as students_router
from app.grades.router import router as grades_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")
    app.state.pool = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    logger.info("Приложение успешно запущено")
    yield
    logger.info("Остановка приложения...")
    await app.state.pool.close()
    logger.info("Приложение остановлено")

app = FastAPI(title="Student Performance API", lifespan=lifespan)

app.include_router(students_router)
app.include_router(grades_router)

@app.get("/health")
async def health():
    logger.debug("Health check запрос")
    return {"status": "ok"}