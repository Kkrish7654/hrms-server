from pydantic import BaseModel, Field


class DesignationBase(BaseModel):
    title: str = Field(..., max_length=255)


class DesignationCreate(DesignationBase):
    pass


class Designation(DesignationBase):
    id: int

    class Config:
        orm_mode = True