from sports_discord.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

tournament_auction_team = Table(
    'tournament_auction_team',
    Base.metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tournament_id', ForeignKey('tournament.id')),
    Column('auction_team_id', ForeignKey('auction_team.id')),
    Column('discord_role_id', Integer, unique=True)
)
