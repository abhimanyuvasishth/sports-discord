from sports_discord.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

tournament_playing_team = Table(
    'tournament_playing_team',
    Base.metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tournament_id', ForeignKey('tournament.id')),
    Column('playing_team_id', ForeignKey('playing_team.id')),
)
