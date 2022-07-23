from sports_discord.database import Base
from sports_discord.models.associations.tournament_auction_team import \
    tournament_auction_team
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, func
from sqlalchemy.orm import relationship


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True, nullable=False)
    series_id = Column(String, nullable=False)
    channel_id = Column(String, unique=True, nullable=False)
    doc_name = Column(String, unique=True, nullable=False)
    points_sheet_name = Column(String, default='Points Worksheet', nullable=False)
    bidding_sheet_name = Column(String, default='Bidding Sheet', nullable=False)
    team_points_name = Column(String, default='Team Points', nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    auction_teams = relationship(
        'AuctionTeam',
        secondary=tournament_auction_team,
        back_populates='tournaments'
    )
