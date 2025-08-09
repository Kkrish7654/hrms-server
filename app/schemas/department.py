from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=255)


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode = True