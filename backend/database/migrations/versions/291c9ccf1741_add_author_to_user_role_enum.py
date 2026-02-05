from alembic import op

revision = "xxxxxxx"
down_revision = "5741e3ff3f7c"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("ALTER TYPE user_role_enum ADD VALUE 'Author'")

def downgrade():
    # PostgreSQL нельзя удалить значение из enum простым способом
    pass