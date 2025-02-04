from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.user.schemas import UserSchema, CreateUserSchema
import app.user.crud as crud

router = APIRouter(prefix='/users', tags=['user'])

# GET ALL USERS
@router.get("", response_model=List[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

# GET USER BY ID
@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_user

#CREATE A USER
@router.post("/register/", response_model=UserSchema)
async def add_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    # checking if username already exists 
    user_exists = crud.get_user_by_username(db=db, username=user.name)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Username already exists")
    # checking if email already exists 
    email_exists = crud.get_user_by_email(db=db, user_email=user.email)
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Email already exists")
    return crud.create_user(user=user, db=db)

#UPDATE A USER
@router.put("/update/{user_id}", response_model=CreateUserSchema)
async def update_user(user_id: int, user: CreateUserSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return crud.update_user(user_id=user_id, user_data=user, db=db)

# DELETE USER BY ID
@router.get("/delete/{user_id}")
async def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return crud.delete_user(user_id=user_id, db=db)


