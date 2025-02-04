from sqlalchemy.orm import Session
from app.models import User
from app.user.schemas import UserSchema, CreateUserSchema
import uuid
from app.password_hashing import Hash
from fastapi import HTTPException, status

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.userid == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.userid == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

def create_user(db: Session, user: UserSchema):

    #Если хотим id в виде хеш-строки
    # user_id =  str(uuid.uuid4())

    # проверка того, существует ли уже такой идентификатор
    # while get_user_by_id(db=db, user_id = user_id):
    #     user_id =  str(uuid.uuid4())

    #hashing password
    password = Hash.get_hashed_password(user.password)

    db_user = User(name=user.name, email=user.email, password=password, roleid=user.roleid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_data: CreateUserSchema):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_data.dict()
        for key, value in update_data.items():
            if key == "password":
                value = Hash.get_hashed_password(value)
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
