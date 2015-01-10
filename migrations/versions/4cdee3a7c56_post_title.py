"""post title

Revision ID: 4cdee3a7c56
Revises: 335fa7983cd
Create Date: 2015-01-09 13:03:09.188450

"""

# revision identifiers, used by Alembic.
revision = '4cdee3a7c56'
down_revision = '335fa7983cd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'title')
    ### end Alembic commands ###