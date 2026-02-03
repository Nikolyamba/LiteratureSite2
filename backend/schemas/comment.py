import uuid
from datetime import datetime

from pydantic import BaseModel


class RequestComment(BaseModel):
    text: str
    target_id: uuid.UUID
    target_type: str


class ResponseComment(RequestComment):
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
