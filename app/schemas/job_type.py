from pydantic import BaseModel, Field


class JobTypeBase(BaseModel):
    type_name: str = Field(..., max_length=100)


class JobTypeCreate(JobTypeBase):
    pass


class JobType(JobTypeBase):
    id: int

    class Config:
        orm_mode = True