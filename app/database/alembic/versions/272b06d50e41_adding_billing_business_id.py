"""adding billing business id

Revision ID: 272b06d50e41
Revises: 227ee0ccd214
Create Date: 2022-01-04 20:12:08.861716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '272b06d50e41'
down_revision = '227ee0ccd214'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inclusion_case', sa.Column('billing_business_id', sa.Integer(), nullable=False))
    op.add_column('inclusion_case', sa.Column('billing_business_name', sa.String(length=120), nullable=False))
    op.create_unique_constraint(None, 'inclusion_case_close', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'inclusion_case_close', type_='unique')
    op.drop_column('inclusion_case', 'billing_business_name')
    op.drop_column('inclusion_case', 'billing_business_id')
    # ### end Alembic commands ###
