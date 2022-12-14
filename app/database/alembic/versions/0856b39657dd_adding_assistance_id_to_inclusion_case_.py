"""adding assistance id to inclusion case table

Revision ID: 0856b39657dd
Revises: c216f2a81572
Create Date: 2021-12-22 07:05:44.884397

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0856b39657dd'
down_revision = 'c216f2a81572'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inclusion_case', sa.Column('assistance_id', sa.Integer(), server_default='1', nullable=False))
    op.add_column('inclusion_case', sa.Column('assistance_names', sa.String(length=120), server_default='ADMIN MYERS', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inclusion_case', 'assistance_names')
    op.drop_column('inclusion_case', 'assistance_id')
    # ### end Alembic commands ###
 
