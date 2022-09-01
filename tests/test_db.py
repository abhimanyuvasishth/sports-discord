import pytest
from sports_discord.models import (Match, MatchPlayer, Player, Team,
                                   Tournament, UserTeam)
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

CHANNEL_ID = '996269799539757056'


@pytest.fixture
def engine():
    return create_engine('sqlite:///sports_discord.db')


@pytest.fixture
def tournament(engine):
    with sessionmaker(engine)() as session:
        return session.query(Tournament).filter(Tournament.channel_id == CHANNEL_ID).first()


def test_user_teams(engine, tournament):
    with sessionmaker(engine)() as session:
        user_teams = session.query(UserTeam).filter(UserTeam.tournament_id == tournament.id).all()
        assert len(user_teams) == 7
        for user_team in user_teams:
            assert user_team.tournament.id == tournament.id


def test_teams(engine, tournament):
    with sessionmaker(engine)() as session:
        teams = session.query(Team).filter(Team.tournament_id == tournament.id).all()
        assert len(teams) == 10
        for team in teams:
            assert team.tournament.id == tournament.id


def test_players(engine, tournament):
    with sessionmaker(engine)() as session:
        player = session.query(Player).first()
        team = session.query(Team).filter(Team.id == player.team_id).first()
        assert team.tournament.id == tournament.id


def test_match(engine):
    with sessionmaker(engine)() as session:
        team_counts = session.query(func.count(Match.id)).group_by(Match.external_id).all()
        assert all([count == 2 for result in team_counts for count in result])


def test_match_player(engine):
    with sessionmaker(engine)() as session:
        mt_query = session.query(Team.id).join(Match).join(MatchPlayer).filter(MatchPlayer.id == 1)
        pt_query = session.query(Team.id).join(Player).join(MatchPlayer).filter(MatchPlayer.id == 1)
        assert mt_query.first() == pt_query.first()
