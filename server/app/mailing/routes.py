from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from mailing.schemas import MailingBase, MailingCreate
import mailing.crud as crud

from auth import get_current_user
from models import User

router = APIRouter(prefix='/mailings', tags=['mailing'])

@router.get("/{mailing_id}", response_model=MailingBase)
def get_mailing(mailing_id: int, db: Session = Depends(get_db)):
    mailing = crud.get_mailing(db, mailing_id)
    if not mailing:
        raise HTTPException(status_code=400, detail="Mailing does not exist")
    return mailing

@router.get("/by_user/{user_id}", response_model=List[MailingBase])
def get_mailings_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_mailings_by_user_id(db, user_id)

@router.get("/", response_model=List[MailingBase])  
def get_mailings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_mailings(db)

@router.post("/create", response_model=MailingCreate)
def create_mailing(mailing: MailingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_mailing(db, mailing, current_user)

@router.put("/update/{mailing_id}", response_model=MailingCreate)
def update_mailing(mailing_id: int, mailing: MailingCreate, db: Session = Depends(get_db)):
    return crud.update_mailing(db, mailing_id, mailing)

@router.delete("/delete/{mailing_id}")
def delete_mailing(mailing_id: int, db: Session = Depends(get_db)):
    return crud.delete_mailing(db, mailing_id)


