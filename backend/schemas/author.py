import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RequestAuthor(BaseModel):
    name: str
    surname: str
    patronimyc: Optional[str] = None
    birthday: Optional[datetime] = None
    about: Optional[str] = None


class ResponseAuthor(RequestAuthor):
    id: uuid.UUID

    class Config:
        from_attributes = True


class GetAuthors(BaseModel):
    id: uuid.UUID
    name: str
    surname: str

    class Config:
        from_attributes = True


class EditAuthor(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronimyc: Optional[str] = None
    birthday: Optional[datetime] = None
    about: Optional[str] = None


