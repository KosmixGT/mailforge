from sqlalchemy.orm import Session
from app.models import Mailinghistory, Mailing
from app.history.schemas import MailingHistoryBase, MailingHistoryCreate
from app.models import User
from app.auth import get_current_user
from datetime import datetime

def get_mailing_history(db: Session, mailing_id: int):
    return db.query(Mailinghistory).filter(Mailinghistory.mailingid == mailing_id).first()

def get_mailing_history_by_id(db: Session, history_id: int):
    return db.query(Mailinghistory).filter(Mailinghistory.historyid == history_id).first()

def create_mailing_history(db: Session, history: MailingHistoryCreate):
    db_history = Mailinghistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history, db_history.historyid

#get all histories by mailings by userid
def get_mailing_histories_by_user(db: Session, user_id: int):
    return db.query(Mailinghistory).join(Mailing).filter(Mailing.userid == user_id).all()



#get_id_mailing_history_by_mailing_and_senttime (return only id)

# def get_id_mailing_history_by_mailing_and_senttime(db: Session, mailing_id: int, senttime: datetime):
#     return db.query(MailingHistoryBase).filter(MailingHistoryBase.mailingid == mailing_id, MailingHistoryBase.senttime == senttime).first()[0]


