from typing import List, Optional, Generic, TypeVar

from pydantic import ConfigDict, BaseModel , Field

from app.config import settings

T = TypeVar('T')

class Request(BaseModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

class UserSchema(BaseModel):
    userid: Optional[int] = None
    name: str
    email: str
    password: str
    roleid: int
    model_config = ConfigDict(from_attributes=True)

class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str
    roleid: int
    model_config = ConfigDict(from_attributes=True)
class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)

class Settings(BaseModel):
    authjwt_secret_key: str = str(settings.SECRET_KEY)