from sports_discord.database import Base
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import relationship


class PlayingTeam(Base):
    __tablename__ = 'playing_team'

    __table_args__ = (
        UniqueConstraint('name', 'tournament_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament', back_populates='playing_teams')
