"""chief expert in event model

Revision ID: 6e7f1a709324
Revises: b0be343c645e
Create Date: 2020-10-30 20:43:49.930391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e7f1a709324'
down_revision = 'b0be343c645e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('chief_expert_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'users', ['chief_expert_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'chief_expert_id')
    # ### end Alembic commands ###
