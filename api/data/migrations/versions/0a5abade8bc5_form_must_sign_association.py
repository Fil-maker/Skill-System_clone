"""form_must_sign_association

Revision ID: 0a5abade8bc5
Revises: e6e627dd6544
Create Date: 2020-12-29 18:30:38.425702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a5abade8bc5'
down_revision = 'e6e627dd6544'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('forms_signatures')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forms_signatures',
    sa.Column('form_to_event_association_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['form_to_event_association_id'], ['form_to_event_association.id'], name='forms_signatures_form_to_event_association_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='forms_signatures_user_id_fkey')
    )
    # ### end Alembic commands ###
