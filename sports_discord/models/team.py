from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sports_discord.database import Base


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    abbrev = Column(String, nullable=False, unique=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')
