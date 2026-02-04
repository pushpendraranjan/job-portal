from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models import Job
from schema import JobCreate, JobUpdate, JobResponse
router = APIRouter()


@router.get("/get_all_jobs",response_model= List[JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/open_jobs_user", response_model= List[JobResponse])
def open_jobs(db:Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.is_open == True).all()
    return jobs

@router.get("/get_by_title", response_model= List[JobResponse])
def get_by_title(title : str, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.title.ilike(f"%{title}%")).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobs not found")
    return jobs

@router.post("/create_job", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
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

router.put ("/update_jobs", response_model= JobResponse)
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    # Fetch the job from the database
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobs not found")

  
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/delete_job")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(db_job)
    db.commit()
    return {"message": f"Job '{db_job.title}' deleted successfully"}