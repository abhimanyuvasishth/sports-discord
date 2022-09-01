import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from sports_discord.models import Match, MatchPlayer, Player, Team, UserTeam


@pytest.fixture
def engine():
    return create_engine('sqlite:///sports_discord.db')


def test_user_teams(engine):
    with sessionmaker(engine)() as session:
        user_teams = session.query(UserTeam).all()
        assert len(user_teams) == 4


def test_teams(engine):
    with sessionmaker(engine)() as session:
        teams = session.query(Team).all()
        assert len(teams) == 6


def test_players(engine):
    with sessionmaker(engine)() as session:
        player = session.query(Player).first()
        _ = session.query(Team).filter(Team.id == player.team_id).first()


def test_match(engine):
    with sessionmaker(engine)() as session:
        team_counts = session.query(func.count(Match.id)).group_by(Match.external_id).all()
        assert all([count == 2 for result in team_counts for count in result])


def test_match_player(engine):
    with sessionmaker(engine)() as session:
        mt_query = session.query(Team.id).join(Match).join(MatchPlayer).filter(MatchPlayer.id == 1)
        pt_query = session.query(Team.id).join(Player).join(MatchPlayer).filter(MatchPlayer.id == 1)
        assert mt_query.first() == pt_query.first()
