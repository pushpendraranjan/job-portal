from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from typing import List
from utils.drivers_utils import upload_to_drive
from db import get_db
from models import Job, Application
from schema import JobResponse

from core.redis_client import redis_job
router = APIRouter()



@router.get("/open_jobs_user", response_model= List[JobResponse])
def open_jobs(db:Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.is_open == True).order_by(Job.id.asc()).all()
    return jobs



@router.post("/{job_id}/apply")
def apply_applicant(
    job_id: int,
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone_no: str = Form(...,pattern=r'^\+91[6-9]\d{9}$',examples=["+915555555555"]),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    #  Check job exists and is open
    job = db.query(Job).filter(Job.id == job_id, Job.is_open == True).first()
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found or closed"
        )
    verified_key = f"verified:{phone_no}"
    
    if redis_job.get(verified_key) != "1":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Phone number not OTP verified")
    
    existing = db.query(Application).filter(Application.phone_no == phone_no).first() #1 apply per job,Application.job_id == job_id
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "You have already applied")

    #     #Upload resume to Google Drive
    # else:
    #     resume_url = upload_to_drive(resume) #.file,# resume.filename,# resume.content_type
#     verified_key = f"verified:{phone_no}"
#     verification_status = redis_job.get(verified_key)

# # Check explicit verification value
#     if verification_status != b"true":   ### redis should return "true" for this change in redisfile
#       raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Phone number not OTP verified"
#     )

    if resume.size > 200 * 1024:
        raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail ="Resume must be less than 200KB")

    resume_url = upload_to_drive(resume)

    if not resume_url:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Failed to upload resume to Google Drive"
            
        )
    
    application = Application(
        name=name,
        email=email,
        phone_no=phone_no,
        resume_url=resume_url,
        job_id=job_id
    )

    db.add(application)
    db.commit()
    redis_job.delete(verified_key)
    db.refresh(application)

    return {"message": "Application submitted successfully"}
