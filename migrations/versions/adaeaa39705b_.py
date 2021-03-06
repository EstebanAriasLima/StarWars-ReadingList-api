"""empty message

Revision ID: adaeaa39705b
Revises: a7e896af477b
Create Date: 2022-02-24 20:00:44.960974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adaeaa39705b'
down_revision = 'a7e896af477b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planet', sa.Column('description', sa.String(length=120), nullable=True))
    op.add_column('vehicle', sa.Column('description', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle', 'description')
    op.drop_column('planet', 'description')
    # ### end Alembic commands ###
