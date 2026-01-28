# import uuid
# from datetime import datetime
#
# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
#
# from backend.models import User
#
# c_router = APIRouter(prefix='/comments')
#
# class RequestComment(BaseModel):
#     text: str
#     target_id: uuid.UUID
#     target_type: str
#
# @c_router.post('')
# async def create_comment(current_user: User = Depends(get_current_user),
#                          )