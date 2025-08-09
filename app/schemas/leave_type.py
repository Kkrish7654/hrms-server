from pydantic import BaseModel, Field


class LeaveTypeBase(BaseModel):
    name: str = Field(..., max_length=100)


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveType(LeaveTypeBase):
    id: int

    class Config:
        orm_mode = True