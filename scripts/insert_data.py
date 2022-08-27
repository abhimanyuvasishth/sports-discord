import json
from os import getenv

from dateutil.parser import parse
from dotenv import load_dotenv
from sports_discord.models import (Match, MatchPlayer, Player, Team,
                                   Tournament, UserTeam, UserTeamPlayer)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine = create_engine(getenv('DATABASE_URL'))


# From scorecard autopopulater scraper
MATCH_CONFIGS = [
    {
        'team_1': 'Chennai Super Kings',
        'team_1_num': 1,
        'team_2': 'Delhi Capitals',
        'team_2_num': 2,
        'start_timestamp': '2022-08-29T00:00:00.000Z',
        'object_id': 1312200
    },
]

# Post Auction scrape from sheet
PLAYER_CONFIGS = [
    {
        'name': 'Ambati Rayudu',
        'team_name': 'Chennai Super Kings',
        'user_team_name': 'Namit',
        'pool': 'A'
    },
    {
        'name': 'Maheesh Theekshana',
        'team_name': 'Chennai Super Kings',
        'user_team_name': 'Shiv, Aryaman',
        'pool': 'B'
    },
    {
        'name': 'Robin Uthappa',
        'team_name': 'Chennai Super Kings',
        'user_team_name': 'Desai, Kush, Naman',
        'pool': 'C'
    },
    {
        'name': 'Anrich Nortje',
        'team_name': 'Delhi Capitals',
        'user_team_name': 'Paro, Rahul, Taro',
        'pool': 'A'
    },
    {
        'name': 'Rovman Powell',
        'team_name': 'Delhi Capitals',
        'user_team_name': 'Shiv, Aryaman',
        'pool': 'B'
    },
    {
        'name': 'Vicky Ostwal',
        'team_name': 'Delhi Capitals',
        'user_team_name': None,
        'pool': 'B'
    },
]


def insert_tournament(tournament_config):
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(Tournament(**tournament_config))


def insert_user_teams(user_team_configs):
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects(
            [UserTeam(**config, tournament_id=1) for config in user_team_configs]
        )


def insert_teams(team_configs):
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects([Team(**config, tournament_id=1) for config in team_configs])


def insert_players():
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in PLAYER_CONFIGS:
            team_id = session.query(Team).filter(Team.name == config['team_name']).first().id
            player = Player(
                name=config['name'],
                team_id=team_id,
                # pool=PlayerPool[config['pool']]
            )
            session.add(player)


def insert_user_team_players():
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in PLAYER_CONFIGS:
            user_team = session.query(UserTeam).filter(
                UserTeam.name == config['user_team_name']
            ).first()
            if not user_team:
                continue
            player_id = session.query(Player).filter(Player.name == config['name']).first().id
            session.add(UserTeamPlayer(player_id=player_id, user_team_id=user_team.id))


def insert_matches():
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in MATCH_CONFIGS:
            match_1 = Match(
                team_id=session.query(Team).filter(Team.name == config['team_1']).first().id,
                external_id=config['object_id'],
                match_num=config['team_1_num'],
                start_timestamp=parse(config['start_timestamp'])
            )
            match_2 = Match(
                team_id=session.query(Team).filter(Team.name == config['team_2']).first().id,
                external_id=config['object_id'],
                match_num=config['team_2_num'],
                start_timestamp=parse(config['start_timestamp'])
            )
            session.bulk_save_objects([match_1, match_2])


def insert_match_players():
    with sessionmaker(engine, autocommit=True).begin() as session:
        for match_config in MATCH_CONFIGS:
            team = session.query(Team).filter(Team.name == match_config['team_1']).first()
            match = session.query(Match).filter(Match.team_id == team.id).first()
            for player_config in PLAYER_CONFIGS:
                if team.name == player_config['team_name']:
                    player = session.query(Player).filter(
                        Player.name == player_config['name']
                    ).first()
                    user_team_player = session.query(UserTeamPlayer).filter(
                        UserTeamPlayer.player_id == player.id
                    ).first()
                    match_player = MatchPlayer(
                        match_id=match.id,
                        player_id=player.id,
                        user_team_player_id=user_team_player.id
                    )
                    session.add(match_player)


if __name__ == '__main__':
    with open('data/asia_cup.json') as f:
        configs = json.loads(f.read())

    insert_tournament(configs['tournament'])
    insert_user_teams(configs['user_teams'])
    insert_teams(configs['teams'])
    # insert_players()
    # insert_user_team_players()
    # insert_matches()
    # insert_match_players()
