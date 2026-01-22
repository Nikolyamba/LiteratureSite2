import uuid
from typing import List

from sqlalchemy import UUID, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True
    )
    genre_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True
    )

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text(500), nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    year_of_publication: Mapped[int] = mapped_column(nullable=True)

    author: Mapped['User'] = relationship(back_populates='books')
    genres: Mapped[List['Genre']] = relationship(secondary='book_genres', back_populates='books')

