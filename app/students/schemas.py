from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    full_name: str = Field(..., example="Курочкин Антон Владимирович")
    group_number: str = Field(..., example="101Б")

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True