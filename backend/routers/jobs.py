from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from typing import List
from utils.drivers_utils import upload_to_drive, file_to_trash
from db import get_db
from models import Job, Application
from schema import JobCreate, JobUpdate, JobResponse, ApplicantAdminView, ApplicantCreate
from security import admin_access
from core.redis_client import redis_job
router = APIRouter()

#applicant 
# @router.get("/open_jobs_user", response_model= List[JobResponse])
# def open_jobs(db:Session = Depends(get_db)):
#     jobs = db.query(Job).filter(Job.is_open == True).order_by(Job.id.asc()).all()
#     return jobs

#apply job
# @router.post("/job/{job_id}/apply") #put
# def apply_applicant(job_id : int, applicant : ApplicantCreate, db : Session = Depends(get_db)):
#     job = db.query(Job).filter(Job.id == job_id, Job.is_open == True).first()
#     if not job :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Job not found or closed")
#     application = Application(
#         **applicant.model_dump(),
#         job_id=job_id
#     )
#     db.add(application)
#     db.commit()
#     db.refresh(application)
#     return application
    
# #View application by admin

@router.get("/{job_id}/applications",response_model=list[ApplicantAdminView])
def view_applications_of_job(job_id: int,db: Session = Depends(get_db), admin = Depends(admin_access)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    applications = db.query(Application).filter(Application.job_id == job_id).all()
    return applications
######


# @router.post("/{job_id}/apply")
# def apply_applicant(
#     job_id: int,
#     name: str = Form(...),
#     email: EmailStr = Form(...),
#     phone_no: str = Form(...,pattern=r'^\+91[6-9]\d{9}$',examples=["+915555555555"]),
#     resume: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     #  Check job exists and is open
#     job = db.query(Job).filter(Job.id == job_id, Job.is_open == True).first()
#     if not job:
#         raise HTTPException(
#             status_code=404,
#             detail="Job not found or closed"
#         )
#     verified_key = f"verified:{phone_no}"
    
#     if redis_job.get(verified_key) != "1":
#         raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Phone number not OTP verified")
    
#     existing = db.query(Application).filter(Application.phone_no == phone_no).first() #1 apply per job,Application.job_id == job_id
#     if existing:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "You have already applied")

#     #     #Upload resume to Google Drive
#     # else:
#     #     resume_url = upload_to_drive(resume) #.file,# resume.filename,# resume.content_type
# #     verified_key = f"verified:{phone_no}"
# #     verification_status = redis_job.get(verified_key)

# # # Check explicit verification value
# #     if verification_status != b"true":   ### redis should return "true" for this change in redisfile
# #       raise HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Phone number not OTP verified"
# #     )

#     if resume.size > 200 * 1024:
#         raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail ="Resume must be less than 200KB")

#     resume_url = upload_to_drive(resume)

#     if not resume_url:
#         raise HTTPException(
#             status_code= status.HTTP_401_UNAUTHORIZED,
#             detail="Failed to upload resume to Google Drive"
            
#         )
    
#     application = Application(
#         name=name,
#         email=email,
#         phone_no=phone_no,
#         resume_url=resume_url,
#         job_id=job_id
#     )

#     db.add(application)
#     db.commit()
#     redis_job.delete(verified_key)
#     db.refresh(application)

#     return {"message": "Application submitted successfully"}



######
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
@router.patch("/update_jobs/{job_id}", response_model=JobResponse)#{job_id}
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

# #
# @router.delete("/delete_job")
# def delete_job(job_id: int, db: Session = Depends(get_db), admin = Depends(admin_access)):
#     db_job = db.query(Job).filter(Job.id == job_id).first()
#     if not db_job:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

#     db.delete(db_job)
#     db.commit()
#     #db.refresh(db_job) ####
#     return {"message": f"Job '{db_job.title}' deleted successfully"}


###
@router.delete("/delete_job/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_access)
):
   
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    job_title = db_job.title

   
    applications = db.query(Application).filter(
        Application.job_id == job_id
    ).all()

   
    for app in applications:
        if app.resume_url:   # you are storing URL, not file_id
            try:
                # Extract file_id from URL
                file_id = app.resume_url.split("/d/")[1].split("/")[0]
                file_to_trash(file_id)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to move resume to trash for application {app.id}"
                )

    try:
        db.delete(db_job)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database deletion failed"
        )

    return {
        "message": f"Job '{job_title}' and its applications deleted."
    }