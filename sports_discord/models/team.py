from sports_discord.database import Base
from sqlalchemy import Column, Integer, String


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    abbrev = Column(String, nullable=False, unique=True)
