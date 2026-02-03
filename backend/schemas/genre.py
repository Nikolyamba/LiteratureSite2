from typing import Optional

from pydantic import BaseModel


class GenreGeneralModel(BaseModel):
    genre_name: str
    image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GetGenres(BaseModel):
    genre_name: str
    image: Optional[str] = None

    class Config:
        from_attributes = True


class EditGenre(BaseModel):
    genre_name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
