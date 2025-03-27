"""Initial migration

Revision ID: 405c83ec2188
Revises: 47eecb2aba3e
Create Date: 2025-03-27 13:02:59.654068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '405c83ec2188'
down_revision: Union[str, None] = '47eecb2aba3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
