from pydantic import BaseModel, Field, ConfigDict


class JobTypeBase(BaseModel):
    type_name: str = Field(..., max_length=100)


class JobTypeCreate(JobTypeBase):
    pass


class JobType(JobTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)