from sports_discord.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    abbrev = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')
