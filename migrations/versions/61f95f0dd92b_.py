"""empty message

Revision ID: 61f95f0dd92b
Revises: 
Create Date: 2021-04-27 13:11:17.941227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61f95f0dd92b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('short_text', sa.String(length=256), nullable=True),
    sa.Column('long_text', sa.Text(), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.Column('source', sa.String(length=128), nullable=True),
    sa.Column('img_url', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    # ### end Alembic commands ###
