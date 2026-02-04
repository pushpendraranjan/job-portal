import os
import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from db import get_db
from models import Admin
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(admin_id: int, level: str) -> str:
    payload = {
        "admin_id": admin_id,
        "level": level,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

security = HTTPBearer()

def get_current_admin(
        credentials: HTTPAuthorizationCredentials = Depends(security), db:Session = Depends(get_db)) -> Admin:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        if payload.get("level") not in ["admin", "superadmin"]:   #["admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        admin = db.query(Admin).filter(Admin.id == payload["admin_id"]).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin not found"
            )
        return admin
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token"
        )
#

# def admin_access(admin: Admin = Depends(get_current_admin)):
#     if admin.level not in ["admin", "superadmin"]:
#         raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Admin access required"
#     )
#     return admin

# def super_admin(admin: Admin = Depends(get_current_admin)):
#     if admin.level != "superadmin":
#         raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="SuperAdmin access required"
#     )
#     return admin


def super_admin(admin: Admin = Depends(get_current_admin)):
    if admin.level != "superadmin":
        raise HTTPException(403, "SuperAdmin access required")
    return admin

def admin_access(admin: Admin = Depends(get_current_admin)):
    if admin.level != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")
    return admin