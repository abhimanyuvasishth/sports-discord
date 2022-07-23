from sports_discord.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship


class UserTeamPlayer(Base):
    __tablename__ = 'user_team_player'

    id = Column(Integer, primary_key=True, nullable=False)
    transfer_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship('Player')
    user_team_id = Column(Integer, ForeignKey('user_team.id'))
    user_team = relationship('UserTeam')
