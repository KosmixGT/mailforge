from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from recipient.schemas import RecipientBase, RecipientCreate
import recipient.crud as crud

from auth import get_current_user
from models import User

router = APIRouter(prefix='/recipients', tags=['recipient'])

@router.get("/{recipient_id}", response_model=RecipientBase)
def get_recipient(recipient_id: int, db: Session = Depends(get_db)):
    recipient = crud.get_recipient(db, recipient_id)
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient does not exist")
    return recipient

@router.get("/", response_model=List[RecipientBase])
def get_recipients(db: Session = Depends(get_db)):
    return crud.get_recipients(db)

@router.post("/create", response_model=RecipientCreate)
def create_recipient(recipient: RecipientCreate, db: Session = Depends(get_db)):
    return crud.create_recipient(db, recipient)

#поиск по mailingid
@router.get("/by_mailing/{mailing_id}", response_model=List[RecipientBase])
def get_recipients_by_mailing_id(mailing_id: int, db: Session = Depends(get_db)):
    return crud.get_recipients_by_mailing_id(db, mailing_id)

#Загрузка получателей из API по идентификатору записи истории
@router.get("/load_recipients/{history_id}")
def load_recipients_from_history(history_id: int, db: Session = Depends(get_db)):
    return crud.get_recipients_by_history_id(db, history_id)
