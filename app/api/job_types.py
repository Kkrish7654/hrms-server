from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.models.job_type import JobType
from app.schemas.job_type import JobTypeCreate, JobType as JobTypeSchema
from app.core.response import success, error

router = APIRouter()

def serialize_job_type(jt: JobType) -> dict:
    return JobTypeSchema.model_validate(jt).model_dump()


@router.post("/", response_model=JobTypeSchema)
async def create_job_type(job_type: JobTypeCreate, db: Session = Depends(get_db_session)):
    db_job_type = JobType(**job_type.model_dump())
    db.add(db_job_type)
    db.commit()
    db.refresh(db_job_type)
    return success(data=serialize_job_type(db_job_type), message="JobType created successfully")


@router.get("/{job_type_id}", response_model=JobTypeSchema)
async def get_job_type(job_type_id: int, db: Session = Depends(get_db_session)):
    db_job_type = db.query(JobType).filter(JobType.id == job_type_id).first()
    if db_job_type is None:
        raise HTTPException(status_code=404, detail="JobType not found")
    return success(data=serialize_job_type(db_job_type), message="JobType retrieved successfully")


@router.get("/", response_model=list[JobTypeSchema])
async def get_job_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    job_types = db.query(JobType).offset(skip).limit(limit).all()
    return success(data=[serialize_job_type(jt) for jt in job_types], message="JobTypes retrieved successfully")


@router.put("/{job_type_id}", response_model=JobTypeSchema)
async def update_job_type(job_type_id: int, job_type: JobTypeCreate, db: Session = Depends(get_db_session)):
    db_job_type = db.query(JobType).filter(JobType.id == job_type_id).first()
    if db_job_type is None:
        raise HTTPException(status_code=404, detail="JobType not found")
    if not job_type.type_name:
        raise HTTPException(status_code=422, detail="Job type name cannot be empty")
    update_data = job_type.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job_type, key, value)
    db.commit()
    db.refresh(db_job_type)
    return success(data=serialize_job_type(db_job_type), message="JobType updated successfully")


@router.delete("/{job_type_id}", response_model=JobTypeSchema)
async def delete_job_type(job_type_id: int, db: Session = Depends(get_db_session)):
    db_job_type = db.query(JobType).filter(JobType.id == job_type_id).first()
    if db_job_type is None:
        raise HTTPException(status_code=404, detail="JobType not found")
    db.delete(db_job_type)
    db.commit()
    return success(data=serialize_job_type(db_job_type), message="JobType deleted successfully")
