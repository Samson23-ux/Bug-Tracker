from typing import Optional
from pydantic import BaseModel

class BugBase(BaseModel):
    title: str
    description: str
    severity: str
    status: str
    reporter: Optional[str] = None
    assignee: Optional[str] = None

class Bug(BugBase):
    id: str

class BugCreate(BugBase):
    pass

class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    reporter: Optional[str] = None
    assignee: Optional[str] = None

class Response(BaseModel):
    message: str
    has_error: Optional[bool] = False
    error_message: Optional[str] = None
    data: Optional[dict | list[dict]] = None
