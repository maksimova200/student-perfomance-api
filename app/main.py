from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import database
from app.students.router import router as students_router
from app.grades.router import router as grades_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Student Performance API", lifespan=lifespan)

app.include_router(students_router)
app.include_router(grades_router)

@app.get("/health")
async def health():
    return {"status": "ok"}