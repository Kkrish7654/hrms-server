from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CompanyUnitBase(BaseModel):
    unit_name: str = Field(..., max_length=255)
    address: Optional[str] = None


class CompanyUnitCreate(CompanyUnitBase):
    pass


class CompanyUnit(CompanyUnitBase):
    id: int

    model_config = ConfigDict(from_attributes=True)