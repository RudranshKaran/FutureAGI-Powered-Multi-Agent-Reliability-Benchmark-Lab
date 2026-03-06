"""add status and total_prompts to experiments

Revision ID: a1b2c3d4e5f6
Revises: 8d90be0ef157
Create Date: 2026-03-05 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str]] = '8d90be0ef157'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add status and total_prompts columns to experiments."""
    op.add_column('experiments', sa.Column('status', sa.String(), nullable=False, server_default='pending'))
    op.add_column('experiments', sa.Column('total_prompts', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    """Remove status and total_prompts columns from experiments."""
    op.drop_column('experiments', 'total_prompts')
    op.drop_column('experiments', 'status')
