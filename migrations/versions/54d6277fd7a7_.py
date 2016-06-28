"""empty message

Revision ID: 54d6277fd7a7
Revises: None
Create Date: 2014-10-26 10:32:11.200585

"""

# revision identifiers, used by Alembic.
revision = '54d6277fd7a7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('sku', sa.Integer(), nullable=False))
    op.drop_column('product', 'shopsku')
    op.drop_column('product', 'shopid')
    op.drop_column('product', 'offername')
    op.alter_column('product', 'image_url',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'image_url',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.add_column('product', sa.Column('offername', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    op.add_column('product', sa.Column('shopid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('product', sa.Column('shopsku', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.drop_column('product', 'sku')
    ### end Alembic commands ###
