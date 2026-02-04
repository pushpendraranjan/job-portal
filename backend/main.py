from fastapi import FastAPI
from db import engine
from models import Base
from jobs import router as auth_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Job Portal API is running"}