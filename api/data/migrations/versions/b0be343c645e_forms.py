"""forms

Revision ID: b0be343c645e
Revises: fb9fa6b298eb
Create Date: 2020-10-19 18:53:45.262509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0be343c645e'
down_revision = 'fb9fa6b298eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_to_event')
    op.add_column('forms', sa.Column('role', sa.SmallInteger(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('forms', 'role')
    op.create_table('user_to_event',
    sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event'], ['events.id'], name='user_to_event_event_fkey'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='user_to_event_user_fkey')
    )
    # ### end Alembic commands ###
