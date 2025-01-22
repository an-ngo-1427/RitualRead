"""empty message

Revision ID: 88d8fe9337c8
Revises: b41638c94680
Create Date: 2025-01-22 12:03:44.618740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88d8fe9337c8'
down_revision = 'b41638c94680'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_password', sa.String(length=200), nullable=False))
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('username')
        batch_op.drop_column('hashed_password')

    # ### end Alembic commands ###
