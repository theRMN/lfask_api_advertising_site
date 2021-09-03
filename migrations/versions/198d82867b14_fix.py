"""fix

Revision ID: 198d82867b14
Revises: eab89691afad
Create Date: 2021-09-03 22:31:47.129602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '198d82867b14'
down_revision = 'eab89691afad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertising', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'advertising', 'creator', ['creator_id'], ['id'])
    op.drop_constraint('creator_advertising_id_fkey', 'creator', type_='foreignkey')
    op.drop_column('creator', 'advertising_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('creator', sa.Column('advertising_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('creator_advertising_id_fkey', 'creator', 'advertising', ['advertising_id'], ['id'])
    op.drop_constraint(None, 'advertising', type_='foreignkey')
    op.drop_column('advertising', 'creator_id')
    # ### end Alembic commands ###