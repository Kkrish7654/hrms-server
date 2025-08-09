from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.leave import Leave
from app.schemas.leave import LeaveCreate, LeaveUpdate, Leave as LeaveSchema
from datetime import date
from app.core.response import success, error

router = APIRouter()

def serialize_leave(l: Leave) -> dict:
    serialized_data = LeaveSchema.model_validate(l).model_dump()
    if 'start_date' in serialized_data and isinstance(serialized_data['start_date'], date):
        serialized_data['start_date'] = serialized_data['start_date'].isoformat()
    if 'end_date' in serialized_data and isinstance(serialized_data['end_date'], date):
        serialized_data['end_date'] = serialized_data['end_date'].isoformat()
    return serialized_data


@router.post("/", response_model=LeaveSchema)
async def create_leave(leave: LeaveCreate, db: Session = Depends(get_db_session)):
    db_leave = Leave(**leave.model_dump())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return success(data=serialize_leave(db_leave), message="Leave created successfully")


@router.get("/{leave_id}", response_model=LeaveSchema)
async def get_leave(leave_id: int, db: Session = Depends(get_db_session)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    return success(data=serialize_leave(db_leave), message="Leave retrieved successfully")


@router.get("/", response_model=list[LeaveSchema])
async def get_leaves(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    leaves = db.query(Leave).offset(skip).limit(limit).all()
    return success(data=[serialize_leave(l) for l in leaves], message="Leaves retrieved successfully")


@router.put("/{leave_id}", response_model=LeaveSchema)
async def update_leave(leave_id: int, leave: LeaveUpdate, db: Session = Depends(get_db_session)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    update_data = leave.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_leave, key, value)
    db.commit()
    db.refresh(db_leave)
    return success(data=serialize_leave(db_leave), message="Leave updated successfully")


@router.delete("/{leave_id}", response_model=LeaveSchema)
async def delete_leave(leave_id: int, db: Session = Depends(get_db_session)):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    db.delete(db_leave)
    db.commit()
    return success(data=serialize_leave(db_leave), message="Leave deleted successfully")
