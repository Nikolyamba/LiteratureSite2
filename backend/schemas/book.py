import uuid
from typing import Optional, List

from pydantic import BaseModel

from backend.schemas.genre import GetGenres


class RegisterBook(BaseModel):
    author_id: uuid.UUID
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    year_of_publication: Optional[int] = None
    genre_ids: List[uuid.UUID] = []


class GetBooks(BaseModel):
    title: str
    image: Optional[str] = None

    class Config:
        from_attributes = True


class ResponseBook(BaseModel):
    author_id: uuid.UUID
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    year_of_publication: Optional[int] = None
    genres: List[GetGenres]

    class Config:
        from_attributes = True


class EditBookData(BaseModel):
    author_id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    year_of_publication: Optional[int] = None
    genre_ids: Optional[List[uuid.UUID]] = None

    class Config:
        from_attributes = True
