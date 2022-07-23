from sports_discord.database import Base
from sports_discord.models.associations.tournament_auction_team import \
    tournament_auction_team
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import relationship


class AuctionTeam(Base):
    __tablename__ = 'auction_team'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    tournaments = relationship(
        'Tournament',
        secondary=tournament_auction_team,
        back_populates='auction_teams'
    )
