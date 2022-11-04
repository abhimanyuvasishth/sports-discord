import os
from datetime import datetime
from functools import cache

from dotenv import load_dotenv
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from sports_discord.models.match import Match
from sports_discord.models.match_player import MatchPlayer
from sports_discord.models.player import Player
from sports_discord.models.user_team import UserTeam

load_dotenv()
engine = create_engine(os.getenv('POSTGRES_URL'))


@cache
def get_user_team_by_id(role_id: str) -> list[UserTeam]:
    with sessionmaker(engine)() as session:
        user_team = session.query(UserTeam).filter(UserTeam.discord_role_id == str(role_id)).first()
        return user_team


def get_old_captain(role_id: str):
    with sessionmaker(engine)() as session:
        match = session.query(Match) \
            .filter(Match.start_timestamp >= datetime.utcnow()) \
            .order_by(Match.start_timestamp).first()

        old_captain = session.query(MatchPlayer.id, Match.match_num, Player.name) \
            .join(Match) \
            .filter(Match.match_day == match.match_day) \
            .join(Player) \
            .join(UserTeam) \
            .filter(UserTeam.discord_role_id == str(role_id)) \
            .filter(MatchPlayer.captain) \
            .first()

        return old_captain


def get_new_captain(role_id: str, player_name: str):
    with sessionmaker(engine)() as session:
        match = session.query(Match) \
            .filter(Match.start_timestamp >= datetime.utcnow()) \
            .order_by(Match.start_timestamp).first()

        new_captain = session.query(MatchPlayer.id, Match.match_num, Player.name) \
            .join(Match) \
            .filter(Match.match_day == match.match_day) \
            .join(Player) \
            .filter(Player.name.ilike(f'%{player_name}%')) \
            .join(UserTeam) \
            .filter(UserTeam.discord_role_id == str(role_id)) \
            .all()

        return new_captain


def get_player_owner(player_name: str):
    with sessionmaker(engine)() as session:
        player_owner = session.query(UserTeam.name, Player.name) \
            .filter(Player.name.ilike(f'%{player_name}%')) \
            .join(UserTeam, UserTeam.id == Player.user_team_id, isouter=True) \
            .all()

        return player_owner


def get_player(player_name: str):
    with sessionmaker(engine)() as session:
        player = session.query(Player) \
            .filter(Player.name.ilike(f'%{player_name}%')) \
            .all()
        return player


def get_player_and_most_recent_match(player_id: int):
    with sessionmaker(engine)() as session:
        player_and_match = session.query(Match.match_num, Player.name) \
            .filter(Player.id == player_id) \
            .join(MatchPlayer, Player.id == MatchPlayer.player_id) \
            .join(Match, Match.id == MatchPlayer.match_id) \
            .filter(Match.start_timestamp <= datetime.utcnow()) \
            .order_by(Match.start_timestamp.desc()) \
            .first()

        return player_and_match


def get_squad(user_team_id: str):
    with sessionmaker(engine)() as session:
        squad = session.query(Player.name) \
            .filter(Player.user_team_id == user_team_id) \
            .all()

        return squad


def get_user_team_by_name(user_team_name: str):
    with sessionmaker(engine)() as session:
        user_team = session.query(UserTeam.id, UserTeam.name) \
            .filter(UserTeam.name.ilike(f'%{user_team_name}%')) \
            .all()

        return user_team


def get_player_out(player_name: str, role_id: str):
    with sessionmaker(engine)() as session:
        player = session.query(Player) \
            .join(UserTeam) \
            .filter(UserTeam.discord_role_id == str(role_id)) \
            .filter(Player.name.ilike(f'%{player_name}%')) \
            .all()
        return player


def get_player_in(player_name: str):
    with sessionmaker(engine)() as session:
        player = session.query(Player) \
            .filter(Player.name.ilike(f'%{player_name}%')) \
            .filter(Player.user_team_id.is_(None)) \
            .all()
        return player


def update_player_user_team(player_id: str, user_team_id):
    with sessionmaker(engine, autocommit=True)() as session:
        update_stmt = (
            update(Player).
            where(Player.id == player_id).
            values(user_team_id=user_team_id)
        )
        session.execute(update_stmt)


def update_captain(match_player_id, flag):
    with sessionmaker(engine, autocommit=True)() as session:
        update_stmt = (
            update(MatchPlayer).
            where(MatchPlayer.id == match_player_id).
            values(captain=flag)
        )
        session.execute(update_stmt)
