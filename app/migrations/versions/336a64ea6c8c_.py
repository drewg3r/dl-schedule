"""empty message

Revision ID: 336a64ea6c8c
Revises: 2356505397aa
Create Date: 2022-01-08 22:35:14.407145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '336a64ea6c8c'
down_revision = '2356505397aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('subject_name_key', 'subject', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('subject_name_key', 'subject', ['name'])
    # ### end Alembic commands ###
