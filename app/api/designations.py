from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.designation import Designation
from app.schemas.designation import DesignationCreate, Designation as DesignationSchema
from app.core.response import success, error

router = APIRouter()

def serialize_designation(d: Designation) -> dict:
    return DesignationSchema.model_validate(d).model_dump()


@router.post("/", response_model=DesignationSchema)
async def create_designation(designation: DesignationCreate, db: Session = Depends(get_db_session)):
    db_designation = Designation(**designation.model_dump())
    db.add(db_designation)
    db.commit()
    db.refresh(db_designation)
    return success(data=serialize_designation(db_designation), message="Designation created successfully")


@router.get("/{designation_id}", response_model=DesignationSchema)
async def get_designation(designation_id: int, db: Session = Depends(get_db_session)):
    db_designation = db.query(Designation).filter(Designation.id == designation_id).first()
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return success(data=serialize_designation(db_designation), message="Designation retrieved successfully")


@router.get("/", response_model=list[DesignationSchema])
async def get_designations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    designations = db.query(Designation).offset(skip).limit(limit).all()
    return success(data=[serialize_designation(d) for d in designations], message="Designations retrieved successfully")


@router.put("/{designation_id}", response_model=DesignationSchema)
async def update_designation(designation_id: int, designation: DesignationCreate, db: Session = Depends(get_db_session)):
    db_designation = db.query(Designation).filter(Designation.id == designation_id).first()
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    if not designation.title:
        raise HTTPException(status_code=422, detail="Designation title cannot be empty")
    update_data = designation.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_designation, key, value)
    db.commit()
    db.refresh(db_designation)
    return success(data=serialize_designation(db_designation), message="Designation updated successfully")


@router.delete("/{designation_id}", response_model=DesignationSchema)
async def delete_designation(designation_id: int, db: Session = Depends(get_db_session)):
    db_designation = db.query(Designation).filter(Designation.id == designation_id).first()
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    db.delete(db_designation)
    db.commit()
    return success(data=serialize_designation(db_designation), message="Designation deleted successfully")
