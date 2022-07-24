"""added match_player

Revision ID: ba5f66c58fda
Revises: 53655ffd2d78
Create Date: 2022-07-24 11:55:41.402525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba5f66c58fda'
down_revision = '53655ffd2d78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('match_player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.String(), nullable=True),
    sa.Column('player_id', sa.String(), nullable=True),
    sa.Column('user_team_player_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['match.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.ForeignKeyConstraint(['user_team_player_id'], ['user_team_player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('match_player')
    # ### end Alembic commands ###
