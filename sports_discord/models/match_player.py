from sqlalchemy import Boolean, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from sports_discord.database import Base


class MatchPlayer(Base):
    __tablename__ = 'match_player'
    __table_args__ = (
        UniqueConstraint('match_id', 'player_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    captain = Column(Boolean, default=False, nullable=False)
    match_id = Column(Integer, ForeignKey('match.id'))
    match = relationship('Match')
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship('Player')
