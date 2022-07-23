"""added player

Revision ID: 65207d33d055
Revises: 9176d6dcb20f
Create Date: 2022-07-23 12:10:41.934306

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '65207d33d055'
down_revision = '9176d6dcb20f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('creation_timestamp', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player')
    # ### end Alembic commands ###
