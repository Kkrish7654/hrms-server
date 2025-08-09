from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.leave import Leave


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    profile_image_url = Column(String(512))
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"))
    joining_date = Column(Date, nullable=False)
    probation_period = Column(String(50))
    work_location_id = Column(Integer, ForeignKey("company_units.id"))
    job_type_id = Column(Integer, ForeignKey("job_types.id"))
    shift_timing = Column(String(100))
    weekly_hours = Column(Numeric(5, 2))
    annual_leave_total = Column(Integer)
    sick_leave_total = Column(Integer)
    casual_leave_total = Column(Integer)
    date_of_birth = Column(Date)
    gender = Column(String(20))
    marital_status = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    salary = Column(Numeric(12, 2))
    currency = Column(String(10))
    pay_frequency = Column(String(50))
    bank_account = Column(String(100))  # Should be encrypted
    bank_name = Column(String(100))
    tax_id = Column(String(100))  # Should be encrypted
    benefits = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    manager = relationship("Employee", remote_side=[id], back_populates="subordinates")
    subordinates = relationship("Employee", back_populates="manager", foreign_keys=[manager_id])
    work_location = relationship("CompanyUnit", back_populates="employees")
    job_type = relationship("JobType", back_populates="employees")
    leaves = relationship("Leave", back_populates="employee", foreign_keys=[Leave.employee_id])
    approved_leaves = relationship("Leave", foreign_keys=[Leave.approved_by_id], back_populates="approver")
    attendance_records = relationship("Attendance", back_populates="employee")