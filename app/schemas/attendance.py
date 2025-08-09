from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    status: str = Field(..., max_length=50)
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    employee_id: Optional[int] = None
    date: Optional[date] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    status: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class Attendance(AttendanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)