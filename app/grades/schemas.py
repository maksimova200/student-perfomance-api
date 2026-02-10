from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime

class GradeCSVRow(BaseModel):
    lesson_date: date
    group_number: str = Field(..., min_length=1, max_length=10)
    full_name: str = Field(..., min_length=3)
    grade: int = Field(..., ge=1, le=5)

    @field_validator("lesson_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            # На всякий случай
            clean_value = str(value).strip()
            return datetime.strptime(clean_value, "%d.%m.%Y").date()
        except Exception:
            raise ValueError(f"Неверный формат даты '{value}', ждем DD.MM.YYYY")

class GradeAnalyticsResponse(BaseModel):
    full_name: str
    count_twos: int