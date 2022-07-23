from sports_discord.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class UserTeam(Base):
    __tablename__ = 'user_team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    discord_role_id = Column(String, nullable=False, unique=True)
    team_points_row = Column(Integer, nullable=False, unique=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')
