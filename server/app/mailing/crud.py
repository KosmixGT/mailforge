from sqlalchemy.orm import Session
from models import Mailing
from mailing.schemas import MailingBase, MailingCreate
from models import User
from auth import get_current_user
from datetime import datetime

def get_mailing(db: Session, mailing_id: int):
    return db.query(Mailing).filter(Mailing.mailingid == mailing_id).first()

def get_mailings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Mailing).offset(skip).limit(limit).all()

def get_mailings_by_user_id(db: Session, user_id: int):
    return db.query(Mailing).filter(Mailing.userid == user_id).all()

def create_mailing(db: Session, mailing: MailingCreate, current_user: User):
    db_mailing = Mailing(**mailing.dict())
    db_mailing.scheduledtime = datetime.now()
    db_mailing.userid = current_user.userid
    db_mailing.statusid = 1
    db.add(db_mailing)
    db.commit()
    db.refresh(db_mailing)
    return db_mailing

def update_mailing(db: Session, mailing_id: int, mailing: MailingCreate):
    db_mailing = get_mailing(db, mailing_id)
    if db_mailing:
        update_data = mailing.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_mailing, key, value)
        db.commit()
        db.refresh(db_mailing)
    return db_mailing

def delete_mailing(db: Session, mailing_id: int):
    db_mailing = get_mailing(db, mailing_id)
    if db_mailing:
        db.delete(db_mailing)
        db.commit()
        return True
    return False