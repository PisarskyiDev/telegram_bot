"""Add innerjoin to relationship

Revision ID: 02527c26eaed
Revises: b6e0afd8fe19
Create Date: 2023-10-19 10:36:50.204008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02527c26eaed'
down_revision: Union[str, None] = 'b6e0afd8fe19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
