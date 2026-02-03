import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from backend.database.session import get_db
from backend.features.auth import get_current_user
from backend.features.rights import isAdmin, can_edit_comment
from backend.models import User, Comment

c_router = APIRouter(prefix='/comments')


class RequestComment(BaseModel):
    text: str
    target_id: uuid.UUID
    target_type: str


class ResponseComment(RequestComment):
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


@c_router.post('', response_model=ResponseComment)
async def create_comment(data: RequestComment, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    new_comment = Comment(text=data.text,
                          target_id=data.target_id,
                          target_type=data.target_type,
                          user_id=current_user.id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return new_comment


@c_router.get("/{user_id}", response_model=List[ResponseComment])
async def get_comments_by_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    if not isAdmin(current_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    q = select(Comment).where(Comment.user_id == user.id)
    result = await db.execute(q)
    comments = result.scalars().all()

    return comments


@c_router.get('', response_model=List[ResponseComment])
async def get_comments_by_target(target_id: uuid.UUID, target_type: str,
                                 db: AsyncSession = Depends(get_db)):
    q = select(Comment).where(
        Comment.target_id == target_id,
        Comment.target_type == target_type
    ).order_by(Comment.created_at).limit(10).offset(10)

    result = await db.execute(q)
    comments = result.scalars().all()

    return comments


@c_router.delete('/{comment_id}')
async def delete_comment(comment_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail='Такой комментарий не найден')

    if not can_edit_comment(current_user, comment.user_id):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    await db.delete(comment)
    await db.commit()

    return {'success': True, 'msg': f'{comment.id} был успешно удалён'}


@c_router.patch('/{comment_id}', response_model=ResponseComment)
async def delete_comment(comment_id: uuid.UUID, text: Optional[str] = None,
                         db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail='Такой комментарий не найден')

    if not can_edit_comment(current_user, comment.user_id):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    if text:
        comment.text = text

    await db.commit()
    await db.refresh(comment)

    return comment
