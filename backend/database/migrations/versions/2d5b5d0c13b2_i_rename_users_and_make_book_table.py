"""i rename users and make book table

Revision ID: 2d5b5d0c13b2
Revises: 729b69b0664f
Create Date: 2026-01-21 13:31:12.211196
"""

from alembic import op
import sqlalchemy as sa


revision = '2d5b5d0c13b2'
down_revision = '729b69b0664f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Переименовать таблицу
    op.rename_table("__users__", "users")

    # Создать таблицу books
    op.create_table(
        "books",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("author_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("year_of_publication", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    # Удалить таблицу books
    op.drop_table("books")

    # Переименовать таблицу обратно
    op.rename_table("users", "__users__")