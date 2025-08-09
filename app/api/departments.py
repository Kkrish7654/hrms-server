from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, Department as DepartmentSchema
from app.core.response import success, error

router = APIRouter()


def serialize_department(dept: Department) -> dict:
    return DepartmentSchema.model_validate(dept).model_dump()


@router.post("/", response_model=DepartmentSchema)
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db_session)):
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return success(data=serialize_department(db_department), message="Department created successfully")


@router.get("/{department_id}", response_model=DepartmentSchema)
async def get_department(department_id: int, db: Session = Depends(get_db_session)):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return success(data=serialize_department(db_department), message="Department retrieved successfully")


@router.get("/", response_model=list[DepartmentSchema])
async def get_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    departments = db.query(Department).offset(skip).limit(limit).all()
    return success(data=[serialize_department(d) for d in departments], message="Departments retrieved successfully")


@router.put("/{department_id}", response_model=DepartmentSchema)
async def update_department(department_id: int, department: DepartmentCreate, db: Session = Depends(get_db_session)):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    update_data = department.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_department, key, value)
    db.commit()
    db.refresh(db_department)
    return success(data=serialize_department(db_department), message="Department updated successfully")


@router.delete("/{department_id}", response_model=DepartmentSchema)
async def delete_department(department_id: int, db: Session = Depends(get_db_session)):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_department)
    db.commit()
    return success(data=serialize_department(db_department), message="Department deleted successfully")
