from fastapi import FastAPI
from db import engine
from models import Base
from jobs import router as job_router
from auth import router as auth_router
# ###
from routers.otp_router import router as otp_router
from dotenv import load_dotenv 
load_dotenv()
#####
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(
    otp_router,
    prefix="/otp",
    tags=["OTP"]
    )

app.include_router(
    job_router,
    prefix ="/jobs",
    tags=["Jobs"])

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

@app.get("/")
def root():
    return {"message": "Job Portal API is running"}