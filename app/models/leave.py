from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type = Column(String(50))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text)
    status = Column(String(50), default="Pending")
    approved_by_id = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="leaves", foreign_keys=[employee_id])
    approver = relationship("Employee", foreign_keys=[approved_by_id], back_populates="approved_leaves")