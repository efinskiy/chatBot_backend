"""Types edit

Revision ID: f55aa394cd17
Revises: 5a980e3e1fa3
Create Date: 2023-10-06 18:52:54.361551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f55aa394cd17'
down_revision: Union[str, None] = '5a980e3e1fa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'attachmenttypes', ['image', 'voice', 'geo', 'file', 'no_attachment'],
                        [('"Message"', 'attachment_type')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'attachmenttypes', ['image', 'voice', 'geo', 'file'],
                        [('"Message"', 'attachment_type')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###
