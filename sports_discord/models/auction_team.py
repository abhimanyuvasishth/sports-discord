from sports_discord.database import Base
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import relationship


class AuctionTeam(Base):
    __tablename__ = 'auction_team'

    __table_args__ = (
        UniqueConstraint('role_id', 'tournament_id'),
        UniqueConstraint('team_name', 'tournament_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(String, nullable=False)
    team_name = Column(String, nullable=False)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament', back_populates='auction_teams')
