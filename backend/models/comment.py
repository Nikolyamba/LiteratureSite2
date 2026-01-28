import uuid
from datetime import datetime

from sqlalchemy import UUID, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=func.now())

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        back_populates='comments',
        foreign_keys=[user_id]
    )

    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship(back_populates='comments')