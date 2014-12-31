"""before markdown server

Revision ID: 1e8340c9796
Revises: 4941da60156
Create Date: 2014-12-31 13:18:16.527208

"""

# revision identifiers, used by Alembic.
revision = '1e8340c9796'
down_revision = '4941da60156'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###