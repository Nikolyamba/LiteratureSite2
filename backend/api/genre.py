import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.book import GetBooks
from backend.database.session import get_db
from backend.features.admin_func import can_edit_genre
from backend.features.auth import get_current_user
from backend.models import User, Genre

g_router = APIRouter(prefix='/genres')

class GenreGeneralModel(BaseModel):
    genre_name: str
    image: Optional[str] = None
    description: Optional[str] = None

@g_router.post('', response_model=GenreGeneralModel)
async def create_genre(data: GenreGeneralModel, current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    if not can_edit_genre(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    q = select(Genre).where(Genre.genre_name == data.genre_name)
    result = await db.execute(q)
    old_genre = result.scalar_one_or_none()
    if old_genre:
        raise HTTPException(status_code=401, detail='Такой жанр уже есть')

    new_genre = Genre(genre_name = data.genre_name,
                      image = data.image,
                      description = data.description)
    db.add(new_genre)
    await db.commit()
    await db.refresh(new_genre)

    return new_genre

class GetGenres(BaseModel):
    genre_name: str
    image: Optional[str] = None
    class Config:
        from_attributes = True


@g_router.get('', response_model=GetGenres)
async def get_all_genres(db: AsyncSession = Depends(get_db)):
    q = select(Genre)
    result = await db.execute(q)
    genres = result.scalars().all()

    return genres

@g_router.get('/{genre_id}', response_model=List[GetBooks])
async def get_genre_books(genre_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
    SELECT title, image FROM books as b
    JOIN book_genres as bg on b.id = bg.book_id
    JOIN genres as g on bg.genre_id = :genre_id
    WHERE g.id = :genre_id
    ORDER BY b.title ASC
    LIMIT 10 OFFSET :offset
    """), {'genre_id': genre_id})
    books = result.fetchall()

    return books


@g_router.delete('/{genre_id}')
async def delete_genre(genre_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> dict:
    q = select(Genre).where(Genre.id == genre_id)
    result = await db.execute(q)
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status_code=404, detail='Такой жанр не найден')

    if not can_edit_genre(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    await db.delete(genre)
    await db.commit()

    return {'success': True, 'msg': 'Жанр успешно удалён'}

class EditGenre(BaseModel):
    genre_name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    class Config:
        from_attributes = True

@g_router.patch('/{genre_id}', response_model=GenreGeneralModel)
async def edit_genre(data: EditGenre, genre_id: uuid.UUID,
                     db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> dict:
    q = select(Genre).where(Genre.id == genre_id)
    result = await db.execute(q)
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status_code=404, detail='Такой жанр не найден')

    if not can_edit_genre(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    update_data = data.model_dump(exclude_unset=True)
    for row, info in update_data.items():
        setattr(genre, row, info)

    await db.commit()
    await db.refresh(genre)

    return genre