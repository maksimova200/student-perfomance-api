from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, datetime
from typing import Any

class GradeCSVRow(BaseModel):
    lesson_date: date
    group_number: str = Field(..., min_length=1, max_length=10)
    full_name: str = Field(..., min_length=3)
    grade: int = Field(..., ge=1, le=5)

    @model_validator(mode="before")
    @classmethod
    def strip_strings(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    data[k] = v.strip()
        return data

    @field_validator("lesson_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(str(value).strip(), "%d.%m.%Y").date()
        except Exception:
            raise ValueError(f"Неверный формат даты '{value}', ждем DD.MM.YYYY")

class GradeAnalyticsResponse(BaseModel):
    full_name: str
    count_twos: int