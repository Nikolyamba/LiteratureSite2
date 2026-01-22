import uuid
from typing import List

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genre_name: Mapped[str] = mapped_column(unique=True, index=True)
    image: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    books: Mapped[List['Book']] = relationship(secondary='book_genres', back_populates='genres')


