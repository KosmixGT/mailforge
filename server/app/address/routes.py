from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.address.schemas import AddressBase, AddressCreate
import app.address.crud as crud

from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix='/addresses', tags=['address'])

@router.get("/{address_id}", response_model=AddressBase)
def get_address(address_id: int, db: Session = Depends(get_db)):
    address = crud.get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=400, detail="Address does not exist")
    return address

@router.get("/", response_model=List[AddressBase])
def get_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)

@router.post("/create", response_model=AddressCreate)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db, address)

#get по типу адреса
@router.get("/by_type/{address_type}", response_model=List[AddressBase])
def get_addresses_by_type(address_type: str, db: Session = Depends(get_db)):
    return crud.get_addresses_by_type(db, address_type)

#get по address
@router.get("/by_address/{address_value}", response_model=List[AddressBase])
def get_addresses_by_address(address_value: str, db: Session = Depends(get_db)):
    return crud.get_addresses_by_address(db, address_value)
