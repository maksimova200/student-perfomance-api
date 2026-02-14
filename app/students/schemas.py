from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    """Базовая схема студента"""
    full_name: str = Field(..., example="Курочкин Антон Владимирович")
    group_number: str = Field(..., example="101Б")

class StudentCreate(StudentBase):
    """Схема для создания студента (наследует все поля из StudentBase)."""
    pass

class StudentResponse(StudentBase):
    """Схема ответа с данными студента, включая ID."""
    id: int

    class Config:
        from_attributes = True


class StudentAnalytics(BaseModel):
    """Схема для аналитики по студентам (количество двоек)."""
    full_name: str
    count_twos: int

    class Config:
        from_attributes = True