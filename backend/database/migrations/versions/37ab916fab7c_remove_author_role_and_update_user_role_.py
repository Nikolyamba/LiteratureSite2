"""remove author role and update user role enum"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "37ab916fab7c"
down_revision = "89499e1d590e"  # <-- ВАЖНО
branch_labels = None
depends_on = None

old_enum = sa.Enum(
    'User',
    'Admin',
    'Author',
    name='user_role_enum'
)

new_enum = sa.Enum(
    'User',
    'Admin',
    name='user_role_enum'
)


def upgrade():
    # 1️⃣ Обновляем данные
    op.execute("""
        UPDATE users
        SET role = 'User'
        WHERE role = 'Author'
    """)

    # 2️⃣ Убираем DEFAULT (ВАЖНО)
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN role DROP DEFAULT
    """)

    # 3️⃣ Переименовываем старый ENUM
    op.execute("""
        ALTER TYPE user_role_enum RENAME TO user_role_enum_old
    """)

    # 4️⃣ Создаём новый ENUM
    new_enum.create(op.get_bind())

    # 5️⃣ Меняем тип колонки
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN role
        TYPE user_role_enum
        USING role::text::user_role_enum
    """)

    # 6️⃣ Возвращаем DEFAULT
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN role SET DEFAULT 'User'
    """)

    # 7️⃣ Удаляем старый ENUM
    op.execute("""
        DROP TYPE user_role_enum_old
    """)



def downgrade():
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN role DROP DEFAULT
    """)

    old_enum.create(op.get_bind())

    op.execute("""
        ALTER TABLE users
        ALTER COLUMN role
        TYPE user_role_enum_old
        USING role::text::user_role_enum_old
    """)

    op.execute("""
        ALTER TABLE users
        ALTER COLUMN role SET DEFAULT 'User'
    """)

    op.execute("DROP TYPE user_role_enum")

    op.execute("""
        ALTER TYPE user_role_enum_old RENAME TO user_role_enum
    """)
