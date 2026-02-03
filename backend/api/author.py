import uuid
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.book import GetBooks
from backend.database.session import get_db
from backend.features.rights import isAdmin
from backend.features.auth import get_current_user
from backend.models import User, Author

a_router = APIRouter(prefix='/authors')

class RequestAuthor(BaseModel):
    name: str
    surname: str
    patronimyc: Optional[str] = None
    birthday: Optional[datetime] = None
    about: Optional[str] = None

class ResponseAuthor(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    patronimyc: Optional[str] = None
    birthday: Optional[datetime] = None
    about: Optional[str] = None

@a_router.post('', response_model=ResponseAuthor)
async def create_author(data: RequestAuthor, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='Отказано в доступе')

    q = select(Author).where(and_(
            Author.name == data.name,
            Author.surname == data.surname
        ))
    result = await db.execute(q)
    old_author = result.scalar_one_or_none()
    if old_author:
        raise HTTPException(status_code=401, detail='Такой автор уже есть')

    if data.birthday:
        data.birthday = data.birthday.strftime("%d-%m-%Y")

    new_author = Author(name = data.name,
                        surname = data.surname,
                        patronimyc = data.patronimyc,
                        birthday = data.birthday,
                        about = data.about)

    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)

    return ResponseAuthor

class GetAuthors(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    class Config:
        from_attributes = True

@a_router.get('', response_model=List[GetAuthors])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    q = select(Author)
    result = await db.execute(q)
    authors = result.scalars().all()

    return authors

@a_router.get('/{author_id}', response_model=List[GetBooks])
async def get_author(author_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
    SELECT title, image FROM books as b
    WHERE b.author_id = :author_id
    ORDER BY b.title ASC
    LIMIT 10 OFFSET :offset
    """), {'author_id': author_id})

    books = result.fetchall()

    return books

@a_router.delete('/{author_id}')
async def delete_author(author_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)) -> dict:
    q = select(Author).where(Author.id == author_id)
    result = await db.execute(q)
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail='Автор не найден')

    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='Отказано в доступе')

    await db.delete(author)
    await db.commit()

    return {'success': True, 'msg': f'{author_id} успешно удалён'}

class EditAuthor(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronimyc: Optional[str] = None
    birthday: Optional[datetime] = None
    about: Optional[str] = None

@a_router.patch('/{author_id}', response_model=ResponseAuthor)
async def edit_author(data: EditAuthor, author_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    q = select(Author).where(Author.id == author_id)
    result = await db.execute(q)
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail='Автор не найден')

    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='Отказано в доступе')

    update_data = data.model_dump(exclude_unset=True)

    for row, info in update_data.items():
        setattr(author, row, info)

    await db.commit()
    await db.refresh(author)

    return author