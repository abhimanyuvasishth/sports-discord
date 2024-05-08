from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from sports_discord.database import Base


class UserTeam(Base):
    __tablename__ = 'user_team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    discord_role_id = Column(String, nullable=False, unique=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')

    def __repr__(self):
        return f'UserTeam(name="{self.name}")'
