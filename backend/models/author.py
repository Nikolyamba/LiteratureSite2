import uuid
from datetime import datetime
from typing import List

from sqlalchemy import UUID, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    patronimyc: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[datetime] = mapped_column(nullable=True)
    about: Mapped[str] = mapped_column(Text(), nullable=True)

    books: Mapped[List['Book']] = relationship(back_populates='author', cascade='all, delete-orphan')
