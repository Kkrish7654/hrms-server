from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, Attendance as AttendanceSchema
from datetime import date
from app.core.response import success, error

router = APIRouter()

def serialize_attendance(att: Attendance) -> dict:
    serialized_data = AttendanceSchema.model_validate(att).model_dump()
    if 'check_in' in serialized_data and isinstance(serialized_data['check_in'], date):
        serialized_data['check_in'] = serialized_data['check_in'].isoformat()
    if 'check_out' in serialized_data and isinstance(serialized_data['check_out'], date):
        serialized_data['check_out'] = serialized_data['check_out'].isoformat()
    if 'date' in serialized_data and isinstance(serialized_data['date'], date):
        serialized_data['date'] = serialized_data['date'].isoformat()
    return serialized_data


@router.post("/", response_model=AttendanceSchema)
async def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db_session)):
    db_attendance = Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return success(data=serialize_attendance(db_attendance), message="Attendance created successfully")


@router.get("/{attendance_id}", response_model=AttendanceSchema)
async def get_attendance(attendance_id: int, db: Session = Depends(get_db_session)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return success(data=serialize_attendance(db_attendance), message="Attendance retrieved successfully")


@router.get("/", response_model=list[AttendanceSchema])
async def get_attendances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    attendances = db.query(Attendance).offset(skip).limit(limit).all()
    return success(data=[serialize_attendance(att) for att in attendances], message="Attendances retrieved successfully")


@router.put("/{attendance_id}", response_model=AttendanceSchema)
async def update_attendance(attendance_id: int, attendance: AttendanceUpdate, db: Session = Depends(get_db_session)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    update_data = attendance.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attendance, key, value)
    db.commit()
    db.refresh(db_attendance)
    return success(data=serialize_attendance(db_attendance), message="Attendance updated successfully")


@router.delete("/{attendance_id}", response_model=AttendanceSchema)
async def delete_attendance(attendance_id: int, db: Session = Depends(get_db_session)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(db_attendance)
    db.commit()
    return success(data=serialize_attendance(db_attendance), message="Attendance deleted successfully")
