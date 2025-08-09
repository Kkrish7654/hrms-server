from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    employee_id: str = Field(..., max_length=50)
    department_id: int
    designation_id: int
    joining_date: date
    profile_image_url: Optional[str] = Field(None, max_length=512)
    manager_id: Optional[int] = None
    probation_period: Optional[str] = Field(None, max_length=50)
    work_location_id: Optional[int] = None
    job_type_id: Optional[int] = None
    shift_timing: Optional[str] = Field(None, max_length=100)
    weekly_hours: Optional[float] = None
    annual_leave_total: Optional[int] = None
    sick_leave_total: Optional[int] = None
    casual_leave_total: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    marital_status: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    salary: Optional[float] = None
    currency: Optional[str] = Field(None, max_length=10)
    pay_frequency: Optional[str] = Field(None, max_length=50)
    bank_account: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=100)
    benefits: Optional[dict] = None
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    employee_id: Optional[str] = Field(None, max_length=50)
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    joining_date: Optional[date] = None
    profile_image_url: Optional[str] = Field(None, max_length=512)
    manager_id: Optional[int] = None
    probation_period: Optional[str] = Field(None, max_length=50)
    work_location_id: Optional[int] = None
    job_type_id: Optional[int] = None
    shift_timing: Optional[str] = Field(None, max_length=100)
    weekly_hours: Optional[float] = None
    annual_leave_total: Optional[int] = None
    sick_leave_total: Optional[int] = None
    casual_leave_total: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    marital_status: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    salary: Optional[float] = None
    currency: Optional[str] = Field(None, max_length=10)
    pay_frequency: Optional[str] = Field(None, max_length=50)
    bank_account: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=100)
    benefits: Optional[dict] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)