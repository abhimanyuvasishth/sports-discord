import json
from os import getenv

from dateutil.parser import parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sports_discord.constants import BIDDING_SHEET_NAME, DOC_NAME, Pool
from sports_discord.google_sheet import get_sheet
from sports_discord.models import Match, MatchPlayer, Player, Team, Tournament, UserTeam

load_dotenv()
engine = create_engine(getenv('POSTGRES_URL'))


def create_tournament(tournament_name):
    with sessionmaker(engine).begin() as session:
        tournament = Tournament(
            name=tournament_name,
        )
        session.add(tournament)

    with sessionmaker(engine).begin() as session:
        return session.query(Tournament).filter(
            Tournament.name == tournament_name
        ).first().id


def insert_user_teams(user_team_configs, tournament_id):
    with sessionmaker(engine).begin() as session:
        session.bulk_save_objects(
            [UserTeam(**dict(config, tournament_id=tournament_id)) for config in user_team_configs]
        )


def insert_teams(team_configs, tournament_id):
    with sessionmaker(engine).begin() as session:
        session.bulk_save_objects(
            [Team(**dict(config, tournament_id=tournament_id)) for config in team_configs]
        )


def create_player_configs():
    player_configs = []
    sheet = get_sheet(DOC_NAME, BIDDING_SHEET_NAME)
    rows = sheet.get_all_values()
    for row in rows[20:1000]:
        if not row[1]:
            continue
        print(row[:10])
        player_configs.append({
            'name': row[1].strip(),
            'team_name': row[2].strip(),
            'pool': Pool[row[6]].value,
            'user_team_name': row[8].strip(),
            'position': 1
        })
    return player_configs


def insert_players(player_configs, tournament_id):
    with sessionmaker(engine).begin() as session:
        for config in player_configs:
            team_id = session.query(Team) \
                .filter(Team.name == config['team_name']) \
                .filter(Team.tournament_id == tournament_id) \
                .first() \
                .id
            user_team = session.query(UserTeam) \
                .filter(UserTeam.name == config['user_team_name']) \
                .filter(UserTeam.tournament_id == tournament_id) \
                .first()
            user_team_id = user_team.id if user_team else None
            player = Player(
                name=config['name'],
                team_id=team_id,
                user_team_id=user_team_id,
                tournament_id=tournament_id,
                pool=config['pool'],
                position=config['position'],
            )
            session.add(player)


def insert_matches(match_configs, tournament_id):
    with sessionmaker(engine).begin() as session:
        for config in match_configs:
            team_1_id = session.query(Team) \
                .filter(Team.name == config['team_1']) \
                .filter(Team.tournament_id == tournament_id) \
                .first() \
                .id
            team_2_id = session.query(Team) \
                .filter(Team.name == config['team_2']) \
                .filter(Team.tournament_id == tournament_id) \
                .first() \
                .id
            match_1 = Match(
                team_id=team_1_id,
                external_id=config['object_id'],
                match_num=config['team_1_num'],
                start_timestamp=parse(config['start_timestamp']),
                match_day=config['match_day'],
                tournament_id=tournament_id
            )
            match_2 = Match(
                team_id=team_2_id,
                external_id=config['object_id'],
                match_num=config['team_2_num'],
                start_timestamp=parse(config['start_timestamp']),
                match_day=config['match_day'],
                tournament_id=tournament_id
            )
            session.bulk_save_objects([match_1, match_2])


def insert_match_players(player_configs, match_configs, tournament_id):
    with sessionmaker(engine).begin() as session:
        for match_config in match_configs:
            for team_key in ['team_1', 'team_2']:
                team = session.query(Team) \
                    .filter(Team.name == match_config[team_key]) \
                    .filter(Team.tournament_id == tournament_id) \
                    .first()
                match = session.query(Match) \
                    .filter(Match.team_id == team.id) \
                    .filter(Match.tournament_id == tournament_id) \
                    .filter(Match.external_id == str(match_config['object_id'])) \
                    .first()
                for player_config in player_configs:
                    if team.name == player_config['team_name']:
                        player = session.query(Player).filter(
                            Player.name == player_config['name']
                        ).first()
                        match_player = MatchPlayer(
                            match_id=match.id,
                            player_id=player.id
                        )
                        session.add(match_player)


if __name__ == '__main__':
    with open('config/world_cup_2024.json') as f:
        configs = json.loads(f.read())

    player_configs = create_player_configs()

    tournament_id = create_tournament(configs['tournament'])
    print(f'Created tournament: {tournament_id}')

    insert_user_teams(configs['user_teams'], tournament_id)
    print(f"Inserted {len(configs['user_teams'])} User Teams")

    insert_teams(configs['teams'], tournament_id)
    print(f"Inserted {len(configs['teams'])} Teams")

    insert_players(player_configs, tournament_id)
    print(f"Inserted {len(player_configs)} Players")

    insert_matches(configs['matches'], tournament_id)
    print(f"Inserted {len(configs['matches'])} Matches")

    insert_match_players(player_configs, configs['matches'], tournament_id)
    print("Inserted Match Players")
