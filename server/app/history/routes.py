from typing import List, Tuple

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime

from app.history.schemas import MailingHistoryBase, MailingHistoryCreate
import app.history.crud as crud

from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix='/history', tags=['MailingHistory'])

@router.get("/{history_id}", response_model=MailingHistoryBase)
def get_mailing_history(history_id: int, db: Session = Depends(get_db)):
    history = crud.get_mailing_history_by_id(db, history_id)
    if not history:
        raise HTTPException(status_code=400, detail="Mailing history does not exist")
    return history

@router.post("/create", response_model=Tuple[MailingHistoryCreate, int])
def create_mailing_history(history: MailingHistoryCreate, db: Session = Depends(get_db)):
    return crud.create_mailing_history(db, history)

#get all histories by userid's mailings
@router.get("/by_user/{user_id}", response_model=List[MailingHistoryBase])
def get_mailing_histories_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_mailing_histories_by_user(db, user_id)





# #get_id_history_by_mailing_and_senttime
# @router.get("/by_mailing_and_senttime/{mailing_id}/{senttime}", response_model=List[MailingHistoryBase])
# def get_mailing_history_by_mailing_and_senttime(mailing_id: int, senttime: datetime, db: Session = Depends(get_db)):
#     return crud.get_id_mailing_history_by_mailing_and_senttime(db, mailing_id, senttime)