from sqlalchemy.orm import Session
from app.models import Address
from app.address.schemas import AddressBase, AddressCreate
from app.models import User
from app.auth import get_current_user
from datetime import datetime

def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.addressid == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Address).offset(skip).limit(limit).all()

def get_addresses_by_type(db: Session, typeid: int):
    return db.query(Address).filter(Address.typeid == typeid).all()

def get_addresses_by_address(db: Session, address: str):
    return db.query(Address).filter(Address.address == address).all()

def create_address(db: Session, address: AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address