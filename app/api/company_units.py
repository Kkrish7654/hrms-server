from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.company_unit import CompanyUnit
from app.schemas.company_unit import CompanyUnitCreate, CompanyUnit as CompanyUnitSchema
from app.core.response import success, error

router = APIRouter()


@router.post("/", response_model=CompanyUnitSchema)
async def create_company_unit(company_unit: CompanyUnitCreate, db: Session = Depends(get_db_session)):
    db_company_unit = CompanyUnit(**company_unit.dict())
    db.add(db_company_unit)
    db.commit()
    db.refresh(db_company_unit)
    return success(data=db_company_unit, message="CompanyUnit created successfully")


@router.get("/{company_unit_id}", response_model=CompanyUnitSchema)
async def get_company_unit(company_unit_id: int, db: Session = Depends(get_db_session)):
    db_company_unit = db.query(CompanyUnit).filter(CompanyUnit.id == company_unit_id).first()
    if db_company_unit is None:
        raise HTTPException(status_code=404, detail="CompanyUnit not found")
    return success(data=db_company_unit, message="CompanyUnit retrieved successfully")


@router.get("/", response_model=list[CompanyUnitSchema])
async def get_company_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    company_units = db.query(CompanyUnit).offset(skip).limit(limit).all()
    return success(data=company_units, message="CompanyUnits retrieved successfully")


@router.put("/{company_unit_id}", response_model=CompanyUnitSchema)
async def update_company_unit(company_unit_id: int, company_unit: CompanyUnitCreate, db: Session = Depends(get_db_session)):
    db_company_unit = db.query(CompanyUnit).filter(CompanyUnit.id == company_unit_id).first()
    if db_company_unit is None:
        raise HTTPException(status_code=404, detail="CompanyUnit not found")
    update_data = company_unit.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_company_unit, key, value)
    db.commit()
    db.refresh(db_company_unit)
    return success(data=db_company_unit, message="CompanyUnit updated successfully")


@router.delete("/{company_unit_id}", response_model=CompanyUnitSchema)
async def delete_company_unit(company_unit_id: int, db: Session = Depends(get_db_session)):
    db_company_unit = db.query(CompanyUnit).filter(CompanyUnit.id == company_unit_id).first()
    if db_company_unit is None:
        raise HTTPException(status_code=404, detail="CompanyUnit not found")
    db.delete(db_company_unit)
    db.commit()
    return success(data=db_company_unit, message="CompanyUnit deleted successfully")
