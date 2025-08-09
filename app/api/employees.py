from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, Employee as EmployeeSchema
from app.core.response import success, error

router = APIRouter()


@router.post("/", response_model=EmployeeSchema)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db_session)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return success(data=db_employee, message="Employee created successfully")


@router.get("/{employee_id}", response_model=EmployeeSchema)
async def get_employee(employee_id: int, db: Session = Depends(get_db_session)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return success(data=db_employee, message="Employee retrieved successfully")


@router.get("/", response_model=list[EmployeeSchema])
async def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return success(data=employees, message="Employees retrieved successfully")


@router.put("/{employee_id}", response_model=EmployeeSchema)
async def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db_session)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    update_data = employee.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return success(data=db_employee, message="Employee updated successfully")


@router.delete("/{employee_id}", response_model=EmployeeSchema)
async def delete_employee(employee_id: int, db: Session = Depends(get_db_session)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return success(data=db_employee, message="Employee deleted successfully")
