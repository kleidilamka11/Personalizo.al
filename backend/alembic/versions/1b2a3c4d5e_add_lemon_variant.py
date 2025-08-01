"""Add lemon_squeezy_variant_id column

Revision ID: 1b2a3c4d5e
Revises: da5b34ce2c14
Create Date: 2025-08-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1b2a3c4d5e'
down_revision = 'da5b34ce2c14'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('song_packages', sa.Column('lemon_squeezy_variant_id', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('song_packages', 'lemon_squeezy_variant_id')
