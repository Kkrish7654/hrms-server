from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.leave_policy import LeavePolicy
from app.schemas.leave_policy import LeavePolicyCreate, LeavePolicy as LeavePolicySchema
from app.core.response import success, error

router = APIRouter()


@router.post("/", response_model=LeavePolicySchema)
async def create_leave_policy(leave_policy: LeavePolicyCreate, db: Session = Depends(get_db_session)):
    db_leave_policy = LeavePolicy(**leave_policy.dict())
    db.add(db_leave_policy)
    db.commit()
    db.refresh(db_leave_policy)
    return success(data=db_leave_policy, message="LeavePolicy created successfully")


@router.get("/{leave_policy_id}", response_model=LeavePolicySchema)
async def get_leave_policy(leave_policy_id: int, db: Session = Depends(get_db_session)):
    db_leave_policy = db.query(LeavePolicy).filter(LeavePolicy.id == leave_policy_id).first()
    if db_leave_policy is None:
        raise HTTPException(status_code=404, detail="LeavePolicy not found")
    return success(data=db_leave_policy, message="LeavePolicy retrieved successfully")


@router.get("/", response_model=list[LeavePolicySchema])
async def get_leave_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    leave_policies = db.query(LeavePolicy).offset(skip).limit(limit).all()
    return success(data=leave_policies, message="LeavePolicies retrieved successfully")


@router.put("/{leave_policy_id}", response_model=LeavePolicySchema)
async def update_leave_policy(leave_policy_id: int, leave_policy: LeavePolicyCreate, db: Session = Depends(get_db_session)):
    db_leave_policy = db.query(LeavePolicy).filter(LeavePolicy.id == leave_policy_id).first()
    if db_leave_policy is None:
        raise HTTPException(status_code=404, detail="LeavePolicy not found")
    update_data = leave_policy.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_leave_policy, key, value)
    db.commit()
    db.refresh(db_leave_policy)
    return success(data=db_leave_policy, message="LeavePolicy updated successfully")


@router.delete("/{leave_policy_id}", response_model=LeavePolicySchema)
async def delete_leave_policy(leave_policy_id: int, db: Session = Depends(get_db_session)):
    db_leave_policy = db.query(LeavePolicy).filter(LeavePolicy.id == leave_policy_id).first()
    if db_leave_policy is None:
        raise HTTPException(status_code=404, detail="LeavePolicy not found")
    db.delete(db_leave_policy)
    db.commit()
    return success(data=db_leave_policy, message="LeavePolicy deleted successfully")
