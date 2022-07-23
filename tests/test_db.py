import pytest
from sports_discord.models.player import Player
from sports_discord.models.team import Team
from sports_discord.models.tournament import Tournament
from sports_discord.models.user_team import UserTeam
from sports_discord.models.user_team_player import UserTeamPlayer
from sqlalchemy import create_engine
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


def test_user_team_players(engine, tournament):
    with sessionmaker(engine)() as session:
        user_team_player = session.query(UserTeamPlayer).first()
        query = session.query(UserTeam).filter(UserTeam.id == user_team_player.user_team_id)
        user_team = query.first()
        assert user_team.tournament.id == tournament.id
