from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models import Job
from schema import JobCreate, JobUpdate, JobResponse
from security import admin_access
router = APIRouter()


@router.get("/open_jobs_user", response_model= List[JobResponse])
def open_jobs(db:Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.is_open == True).order_by(Job.id.asc()).all()
    return jobs

@router.get("/User_search_jobs_by_title", response_model= List[JobResponse])
def user_title(title : str, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.title.ilike(f"%{title}%"), Job.is_open == True).order_by(Job.id.asc()).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobs not found")
    return jobs

@router.get("/get_all_jobs",response_model= List[JobResponse])
def get_all_jobs(db: Session = Depends(get_db), admin = Depends(admin_access)):
    jobs = db.query(Job).order_by(Job.id.asc()).all()
    return jobs

@router.get("/get_by_title", response_model= List[JobResponse])
def get_by_title(title : str, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.title.ilike(f"%{title}%")).order_by(Job.id.asc()).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobs not found")
    return jobs

@router.post("/create_job", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db), admin = Depends(admin_access)):
    new_job = Job(
        type=job.type,
        title=job.title,
        description=job.description,
        min_experience=job.min_experience,
        max_experience=job.max_experience,
        location=job.location,
        mode=job.mode,
        compensation=job.compensation,
        compensation_type=job.compensation_type,
        is_open=job.is_open
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

# @router.post("/update_jobs", response_model= JobResponse)
# def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db), admin = Depends(admin_access)):
#     # Fetch job from db
#     db_job = db.query(Job).filter(Job.id == job_id).first()
#     if not db_job:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobs not found")
#     # for key, value in job_update.model_dump(exclude_unset=True).items():
#     #     setattr(db_job, key, value)

  
#     for key, value in job_update.dict(exclude_unset=True).items():
#         setattr(db_job, key, value)

#     db.commit()
#     db.refresh(db_job)
#     return db_job
#
@router.patch("/update_jobs", response_model=JobResponse)#{job_id}
def update_job(job_id: int,job_update: JobUpdate,db: Session = Depends(get_db),
    admin = Depends(admin_access)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in job_update.model_dump(exclude_unset=True).items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)
    return db_job

#
@router.delete("/delete_job")
def delete_job(job_id: int, db: Session = Depends(get_db), admin = Depends(admin_access)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(db_job)
    db.commit()
    db.refresh(db_job)
    return {"message": f"Job '{db_job.title}' deleted successfully"}