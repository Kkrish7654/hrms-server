from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class LeaveBase(BaseModel):
    employee_id: int
    leave_type: str = Field(..., max_length=50)
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: str = Field("Pending", max_length=50)
    approved_by_id: Optional[int] = None


class LeaveCreate(LeaveBase):
    pass


class Leave(LeaveBase):
    id: int

    class Config:
        orm_mode = True