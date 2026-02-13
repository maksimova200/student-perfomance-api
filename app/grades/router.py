from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from asyncpg import Connection
from app.utils.csv_parser import parse_csv
from app.grades.repository import bulk_insert_grades
from app.database import get_connection

router = APIRouter(tags=["Grades"])

@router.post("/upload-grades")
async def upload_grades(
    file: UploadFile = File(...),
    conn: Connection = Depends(get_connection)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Файл должен быть формата .csv")

    try:
        content_bytes = await file.read()
        content_str = content_bytes.decode("utf-8-sig")
        rows = parse_csv(content_str)
        result = await bulk_insert_grades(rows, conn)
        return {"status": "ok", "details": result}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")