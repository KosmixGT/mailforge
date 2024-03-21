from typing import List, Optional, Generic, TypeVar

from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

from config import settings

T = TypeVar('T')

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

class UserSchema(BaseModel):
    userid: Optional[int]
    name: str
    email: str
    password: str
    roleid: int

    class Config:
        orm_mode = True

class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str
    roleid: int

    class Config:
        from_attributes = True
        
class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)

class Settings(BaseModel):
    authjwt_secret_key: str = str(settings.SECRET_KEY)