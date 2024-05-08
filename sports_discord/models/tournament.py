from sqlalchemy import Column, Integer, String

from sports_discord.database import Base


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
