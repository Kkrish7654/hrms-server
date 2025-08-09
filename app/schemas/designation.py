from pydantic import BaseModel, Field, ConfigDict


class DesignationBase(BaseModel):
    title: str = Field(..., max_length=255)


class DesignationCreate(DesignationBase):
    pass


class Designation(DesignationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)