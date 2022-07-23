import pytest
from sports_discord.models.tournament import Tournament
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CHANNEL_ID = '996269799539757056'


@pytest.fixture
def engine():
    return create_engine('sqlite:///sports_discord.db')


def test_auction_teams(engine):
    with sessionmaker(engine)() as session:
        tournament = session.query(Tournament).filter(Tournament.channel_id == CHANNEL_ID).first()
        assert len(tournament.auction_teams) == 7
        for team in tournament.auction_teams:
            assert tournament in team.tournaments


def test_playing_teams(engine):
    with sessionmaker(engine)() as session:
        tournament = session.query(Tournament).filter(Tournament.channel_id == CHANNEL_ID).first()
        assert len(tournament.playing_teams) == 10
        for team in tournament.playing_teams:
            assert tournament in team.tournaments
