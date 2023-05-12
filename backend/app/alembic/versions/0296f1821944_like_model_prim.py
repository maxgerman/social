"""Like model prim

Revision ID: 0296f1821944
Revises: 9bb2a2980221
Create Date: 2023-05-12 03:18:53.656730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0296f1821944'
down_revision = '9bb2a2980221'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_primary_key('pkey', 'like', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('pkey', 'like', type_='primary')
    # ### end Alembic commands ###
