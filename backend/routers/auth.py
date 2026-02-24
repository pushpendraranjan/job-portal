from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
#from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db
from models import Admin
from schema import AdminLoginResponse, AdminCreate, AdminLogin
from security import hash_password, verify_password, create_access_token,super_admin #, admin_access
router = APIRouter()

#

# @router.put("/create-superadmin")
# def create_admin(admin: AdminCreate ,db: Session = Depends(get_db)):   #
#     existing_user = db.query(Admin).filter(Admin.email == admin.email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )

#     hashed_password = hash_password(admin.password)

#     new_admin = Admin(
#         name=admin.name,
#         email=admin.email,
#         hashed_password=hashed_password, 
#         level="superadmin"
#     )

#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)

#     return {
#         "message":f"{new_admin.name}, is now an {new_admin.level}"
#     }
# #

@router.put("/create-admin")
def create_admin(admin: AdminCreate ,db: Session = Depends(get_db),current_admin: Admin = Depends(super_admin)):   #
    existing_user = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(admin.password)

    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=hashed_password, 
        level="admin"
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {
        "message":f"{new_admin.name}, is now an admin"
    }

@router.post("/login-admin", response_model= AdminLoginResponse)
def login_admin(admin : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): #,current_admin:Admin = Depends(admin_access) //admin: AdminLogin, 
    db_admin = db.query(Admin).filter(Admin.email == admin.username).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(admin.password, db_admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password"
        )

    token = create_access_token(
        admin_id= db_admin.id,
        level = db_admin.level
    )

    return {
        "message": f"Hello {db_admin.name}, {db_admin.level}, welcome back",
        "access_token": token,
        "token_type": "bearer"
    }

