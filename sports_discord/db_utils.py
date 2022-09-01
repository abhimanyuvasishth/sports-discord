import os
from datetime import datetime
from dotenv import load_dotenv
from functools import cache
from typing import Optional

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from sports_discord.models.match import Match
from sports_discord.models.match_player import MatchPlayer
from sports_discord.models.player import Player
from sports_discord.models.tournament import Tournament
from sports_discord.models.user_team import UserTeam

load_dotenv()
engine = create_engine(os.getenv('POSTGRES_URL'))


@cache
def get_tournament(channel_id: str) -> Optional[Tournament]:
    with sessionmaker(engine)() as session:
        return session.query(Tournament).filter(Tournament.channel_id == str(channel_id)).first()


@cache
def get_user_team(role_id: str) -> list[UserTeam]:
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
            .filter(Match.external_id == match.external_id) \
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
            .filter(Match.external_id == match.external_id) \
            .join(Player) \
            .filter(Player.name.ilike(f'%{player_name}%')) \
            .join(UserTeam) \
            .filter(UserTeam.discord_role_id == str(role_id)) \
            .all()

        return new_captain


def update_captain(match_player_id, flag):
    with sessionmaker(engine, autocommit=True)() as session:
        update_stmt = (
            update(MatchPlayer).
            where(MatchPlayer.id == match_player_id).
            values(captain=flag)
        )
        session.execute(update_stmt)
