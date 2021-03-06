"""init

Revision ID: 41e611b4be20
Revises: 
Create Date: 2019-10-22 17:59:34.515205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41e611b4be20'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_models'))
    )
    op.create_index('my_index', 'models', ['name'], unique=True, mysql_length=255)
    op.create_unique_constraint(op.f('uq_user_email'), 'user', ['email'])
    op.create_unique_constraint(op.f('uq_user_username'), 'user', ['username'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_user_username'), 'user', type_='unique')
    op.drop_constraint(op.f('uq_user_email'), 'user', type_='unique')
    op.drop_index('my_index', table_name='models')
    op.drop_table('models')
    # ### end Alembic commands ###
