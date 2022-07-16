"""create tournament table

Revision ID: 17dad96dc3c9
Revises: None
Create Date: 2022-07-14 12:37:24.557651

"""
from alembic import op
from sqlalchemy import BOOLEAN, INTEGER, TEXT, TIMESTAMP, VARCHAR, Column, func
from sqlalchemy.schema import DefaultClause

# revision identifiers, used by Alembic.
revision = '17dad96dc3c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tournament',
        Column('id', INTEGER, primary_key=True),
        Column('series_id', VARCHAR(100)),
        Column('channel_id', VARCHAR(100), unique=True),
        Column('doc_name', TEXT),
        Column('points_sheet_name', TEXT),
        Column('bidding_sheet_name', TEXT),
        Column('team_points_sheet_name', TEXT),
        Column('sheet_url', TEXT),
        Column('active', BOOLEAN, server_default=DefaultClause("1")),
        Column('creation_timestamp', TIMESTAMP, server_default=func.now()),
    )


def downgrade() -> None:
    op.drop_table('tournament')
