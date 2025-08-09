from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.leave_type import LeaveType
from app.schemas.leave_type import LeaveTypeCreate, LeaveType as LeaveTypeSchema
from app.core.response import success, error

router = APIRouter()


@router.post("/", response_model=LeaveTypeSchema)
async def create_leave_type(leave_type: LeaveTypeCreate, db: Session = Depends(get_db_session)):
    db_leave_type = LeaveType(**leave_type.dict())
    db.add(db_leave_type)
    db.commit()
    db.refresh(db_leave_type)
    return success(data=db_leave_type, message="LeaveType created successfully")


@router.get("/{leave_type_id}", response_model=LeaveTypeSchema)
async def get_leave_type(leave_type_id: int, db: Session = Depends(get_db_session)):
    db_leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if db_leave_type is None:
        raise HTTPException(status_code=404, detail="LeaveType not found")
    return success(data=db_leave_type, message="LeaveType retrieved successfully")


@router.get("/", response_model=list[LeaveTypeSchema])
async def get_leave_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    leave_types = db.query(LeaveType).offset(skip).limit(limit).all()
    return success(data=leave_types, message="LeaveTypes retrieved successfully")


@router.put("/{leave_type_id}", response_model=LeaveTypeSchema)
async def update_leave_type(leave_type_id: int, leave_type: LeaveTypeCreate, db: Session = Depends(get_db_session)):
    db_leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if db_leave_type is None:
        raise HTTPException(status_code=404, detail="LeaveType not found")
    update_data = leave_type.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_leave_type, key, value)
    db.commit()
    db.refresh(db_leave_type)
    return success(data=db_leave_type, message="LeaveType updated successfully")


@router.delete("/{leave_type_id}", response_model=LeaveTypeSchema)
async def delete_leave_type(leave_type_id: int, db: Session = Depends(get_db_session)):
    db_leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if db_leave_type is None:
        raise HTTPException(status_code=404, detail="LeaveType not found")
    db.delete(db_leave_type)
    db.commit()
    return success(data=db_leave_type, message="LeaveType deleted successfully")
