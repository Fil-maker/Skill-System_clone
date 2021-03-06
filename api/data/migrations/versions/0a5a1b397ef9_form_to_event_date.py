"""form to event: date

Revision ID: 0a5a1b397ef9
Revises: 2f28266c98af
Create Date: 2020-11-25 17:00:14.087833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a5a1b397ef9'
down_revision = '2f28266c98af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('form_to_event_association', sa.Column('date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('form_to_event_association', 'date')
    # ### end Alembic commands ###
