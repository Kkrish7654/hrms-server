from pydantic import BaseModel, Field, ConfigDict


class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=255)


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)