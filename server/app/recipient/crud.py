from sqlalchemy.orm import Session
from models import Recipient
from recipient.schemas import RecipientBase, RecipientCreate
from models import User
from auth import get_current_user
from datetime import datetime

def get_recipient(db: Session, recipient_id: int):
    return db.query(Recipient).filter(Recipient.recipientid == recipient_id).first()

def get_recipients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recipient).offset(skip).limit(limit).all()

def create_recipient(db: Session, recipient: RecipientCreate):
    db_recipient = Recipient(**recipient.dict())
    db.add(db_recipient)
    db.commit()
    db.refresh(db_recipient)
    return db_recipient

def get_recipients_by_mailing_id(db: Session, mailing_id: int):
    return db.query(Recipient).filter(Recipient.mailingid == mailing_id).all()

