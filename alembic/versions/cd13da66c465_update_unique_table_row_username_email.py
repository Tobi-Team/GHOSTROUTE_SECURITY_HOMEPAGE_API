"""update unique table row - username, email

Revision ID: cd13da66c465
Revises: 1b9d874324ba
Create Date: 2025-03-02 23:25:59.642083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd13da66c465'
down_revision: Union[str, None] = '1b9d874324ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'], schema='public')
    op.create_unique_constraint(None, 'users', ['username'], schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', schema='public', type_='unique')
    op.drop_constraint(None, 'users', schema='public', type_='unique')
    # ### end Alembic commands ###
