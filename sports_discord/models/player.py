from sports_discord.database import Base
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String, func)
from sqlalchemy.orm import relationship


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship('Team')
