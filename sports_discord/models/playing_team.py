from sports_discord.database import Base
from sports_discord.models.associations.tournament_playing_team import \
    tournament_playing_team
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import relationship


class PlayingTeam(Base):
    __tablename__ = 'playing_team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    abbrev = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    tournaments = relationship(
        'Tournament',
        secondary=tournament_playing_team,
        back_populates='playing_teams'
    )
