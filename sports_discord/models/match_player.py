from sports_discord.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship


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
