from sports_discord.models.tournament import Tournament
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CHANNEL_ID = '996269799539757056'


def test_tournament_teams():
    engine = create_engine('sqlite:///sports_discord.db')
    with sessionmaker(engine)() as session:
        tournament = session.query(Tournament).filter(Tournament.channel_id == CHANNEL_ID).first()
        assert len(tournament.auction_teams) == 7
        for team in tournament.auction_teams:
            assert tournament in team.tournaments
