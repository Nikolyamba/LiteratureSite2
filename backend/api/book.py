import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.genre import GetGenres
from backend.database.session import get_db
from backend.features.rights import isAdmin
from backend.features.auth import get_current_user
from backend.models import User, Book, Genre

b_router = APIRouter(prefix = '/books')

class RegisterBook(BaseModel):
    author_id: uuid.UUID
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    year_of_publication: Optional[int] = None
    genre_ids: List[uuid.UUID] = []

@b_router.post('', response_model=RegisterBook)
async def new_book(data: RegisterBook, current_user: User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    q = select(Book).where(
        and_(
            Book.title == data.title,
            Book.author_id == data.author_id
        )
    )
    result = await db.execute(q)
    old_book = result.scalar_one_or_none()

    if old_book:
        raise HTTPException(status_code=409, detail='Такая книга уже есть на сайте!')

    new_book = Book(author_id=data.author_id,
                    title=data.title,
                    description=data.description,
                    image=data.image,
                    year_of_publication=data.year_of_publication)

    if data.genre_ids:
        q_genre = select(Genre).where(Genre.id.in_(data.genre_ids))
        result_genre = await db.execute(q_genre)
        genres = result_genre.scalars().all()
        if len(genres) != len(set(data.genres)):
            raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")

        new_book.genres = genres

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    return new_book

class GetBooks(BaseModel):
    title: str
    image: Optional[str] = None
    class Config:
        from_attributes = True

@b_router.get('', response_model=GetBooks)
async def get_all_books(db: AsyncSession = Depends(get_db)):
    q = select(Book)
    result = await db.execute(q)
    books = result.scalars().all()

    return books

class ResponseBook(BaseModel):
    author_id: uuid.UUID
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    year_of_publication: Optional[int] = None
    genres: List[GetGenres]
    class Config:
        from_attributes=True


@b_router.get('/{book_id}', response_model=ResponseBook)
async def get_book(book_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    q = (
        select(Book)
        .where(Book.id == book_id)
        .options(selectinload(Book.genres))
    )
    result = await db.execute(q)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail='Такая книга не найдена!')

    return book

@b_router.delete('/{book_id}')
async def del_book(book_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> dict:
    q = select(Book).where(Book.id == book_id)
    result = await db.execute(q)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail='Такая книга не найдена!')

    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    await db.delete(book)
    await db.commit()

    return {'success': True, 'msg': 'Книга успешно удалена'}

class EditBookData(BaseModel):
    author_id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    year_of_publication: Optional[int] = None
    genre_ids: Optional[List[uuid.UUID]] = None
    class Config:
        from_attributes = True

@b_router.patch('/{book_id}', response_model=RegisterBook)
async def edit_book(book_id: uuid.UUID, data: EditBookData, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    q = select(Book).where(Book.id == book_id).options(selectinload(Book.genres))
    result = await db.execute(q)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail='Такая книга не найдена!')

    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    update_data = data.model_dump(exclude_unset=True)
    for row, info in update_data.items():
        if row != 'genre_ids':
            setattr(book, row, info)

    if 'genre_ids' in update_data:
        genre_ids = update_data.get('genre_ids')

        if genre_ids is not None:
            genre_ids = list(set(genre_ids))

            genres_q = select(Genre).where(Genre.id.in_(genre_ids))
            genres = (await db.execute(genres_q)).scalars().all()

            if len(genres) != len(genre_ids):
                raise HTTPException(
                    status_code=400,
                    detail="Некоторые жанры не найдены"
                )

            book.genres = genres

    await db.commit()
    await db.refresh(book)

    return book


