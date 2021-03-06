"""empty message

Revision ID: 09888c54b6f5
Revises: 
Create Date: 2020-10-06 20:43:21.787932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09888c54b6f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.SmallInteger(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
