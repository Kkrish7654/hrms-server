from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CompanyUnit(Base):
    __tablename__ = "company_units"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_name = Column(String(255), unique=True, nullable=False)
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employees = relationship("Employee", back_populates="work_location")