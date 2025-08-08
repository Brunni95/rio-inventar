"""add room column to assets

Revision ID: 20250808_add_room
Revises: 74d730be9ee6
Create Date: 2025-08-08
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250808_add_room'
down_revision = '74d730be9ee6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('assets', sa.Column('room', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('assets', 'room')


