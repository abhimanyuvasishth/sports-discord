from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from sports_discord.database import Base


class Match(Base):
    __tablename__ = 'match'
    __table_args__ = (
        UniqueConstraint('external_id', 'team_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    external_id = Column(String, nullable=False)
    start_timestamp = Column(TIMESTAMP, nullable=False)
    match_num = Column(Integer, nullable=False)
    match_day = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship('Team')
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')
