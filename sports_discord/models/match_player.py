from sports_discord.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class MatchPlayer(Base):
    __tablename__ = 'match_player'

    id = Column(Integer, primary_key=True, nullable=False)
    match_id = Column(Integer, ForeignKey('match.id'))
    match = relationship('Match')
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship('Player')
    user_team_player_id = Column(Integer, ForeignKey('user_team_player.id'))
    user_team_player = relationship('UserTeamPlayer')
