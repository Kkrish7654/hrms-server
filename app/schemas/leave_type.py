from pydantic import BaseModel, Field, ConfigDict


class LeaveTypeBase(BaseModel):
    name: str = Field(..., max_length=100)


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveType(LeaveTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)