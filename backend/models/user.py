import uuid
from enum import Enum as PyEnum

from sqlalchemy import UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base

class UserRole(PyEnum):
    user: str = "User"
    admin: str = "Admin" #ВРУЧНУЮ ЗАТЕМ НАДО РАСШИРЯТЬ ЭНАМ

class User(Base):
    __tablename__ = "__users__"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role_enum",
            values_callable=lambda enum: [e.value for e in enum]
        ),
        default=UserRole.user,
        server_default=UserRole.user.value,
        nullable=False
    )
    info:  Mapped[str] = mapped_column(nullable=True)

