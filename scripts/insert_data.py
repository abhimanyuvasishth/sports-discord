import json
from os import getenv

from dateutil.parser import parse
from dotenv import load_dotenv
from sports_discord.models import (Match, MatchPlayer, Player, Team,
                                   Tournament, UserTeam, UserTeamPlayer)
from sports_discord.google_sheet import get_sheet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine = create_engine(getenv('POSTGRES_URL'))


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


def create_player_configs():
    player_configs = []
    sheet = get_sheet('Asia Cup 2022', 'Bidding Page')
    rows = sheet.get_all_values()
    for row in rows[20:64]:
        player_configs.append({
            'name': row[1],
            'team_name': row[2],
            'user_team_name': row[8]
        })
    return player_configs


def insert_players(player_configs):
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in player_configs:
            team_id = session.query(Team).filter(Team.name == config['team_name']).first().id
            player = Player(
                name=config['name'],
                team_id=team_id,
            )
            session.add(player)


def insert_user_team_players(player_configs):
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in player_configs:
            user_team = session.query(UserTeam).filter(
                UserTeam.name == config['user_team_name']
            ).first()
            if not user_team:
                continue
            player_id = session.query(Player).filter(Player.name == config['name']).first().id
            session.add(UserTeamPlayer(player_id=player_id, user_team_id=user_team.id))


def insert_matches(match_configs):
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in match_configs:
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


def insert_match_players(player_configs, match_configs):
    with sessionmaker(engine, autocommit=True).begin() as session:
        for match_config in match_configs:
            team = session.query(Team).filter(Team.name == match_config['team_1']).first()
            match = session.query(Match).filter(Match.team_id == team.id).first()
            for player_config in player_configs:
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

    player_configs = create_player_configs()
    insert_players(player_configs)
    insert_user_team_players(player_configs)
    insert_matches(configs['matches'])
    insert_match_players(player_configs, configs['matches'])
