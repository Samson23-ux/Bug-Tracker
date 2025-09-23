from typing import Optional
from pydantic import BaseModel

class AccountBase(BaseModel):
    username: str
    password: str
    role: str

class Account(AccountBase):
    id: str

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    username: Optional[str] = None
    password: str
    role: Optional[str] = None

class Response(BaseModel):
    message: str
    has_error: Optional[bool] = False
    error_message: Optional[str] = None
    data: Optional[dict | list[dict]] = None
