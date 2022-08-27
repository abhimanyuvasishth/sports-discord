import os
from dotenv import load_dotenv
from functools import cache
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
