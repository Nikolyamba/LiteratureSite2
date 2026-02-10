from typing import Annotated, Optional

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    login: str
    password: Annotated[str, Field(min_length=8, max_length=128)]
    email: str


class LoginSchema(BaseModel):
    login: str
    password: str


class GetAllUsers(BaseModel):
    login: str
    image: Optional[str] = None

    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    login: str
    image: Optional[str] = None
    info: Optional[str] = None

    class Config:
        from_attributes = True


class EditUserData(BaseModel):
    login: Optional[str] = None
    image: Optional[str] = None
    info: Optional[str] = None
    password: Optional[Annotated[str, Field(min_length=8, max_length=128)]] = None

    class Config:
        from_attributes = True
