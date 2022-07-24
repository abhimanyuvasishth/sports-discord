from dateutil.parser import parse
from sports_discord.models import (Match, MatchPlayer, Player, Team,
                                   Tournament, UserTeam, UserTeamPlayer)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

channel_id = '996269799539757056'
engine = create_engine('sqlite:///sports_discord.db')

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
PLAYER_CONFIGS = [
    {
        'name': 'Ambati Rayudu',
        'team_name': 'Chennai Super Kings',
        'user_team_name': 'Namit',
        'points_row': 6,
        'bidding_row': 47,
    },
    {
        'name': 'Maheesh Theekshana',
        'team_name': 'Chennai Super Kings',
        'user_team_name': 'Shiv, Aryaman',
        'points_row': 19,
        'bidding_row': 144,
    },
    {
        'name': 'Robin Uthappa',
        'team_name': 'Chennai Super Kings',
        'user_team_name': 'Desai, Kush, Naman',
        'points_row': 24,
        'bidding_row': 127,
    },
    {
        'name': 'Anrich Nortje',
        'team_name': 'Delhi Capitals',
        'user_team_name': 'Paro, Rahul, Taro',
        'points_row': 34,
        'bidding_row': 51,
    },
    {
        'name': 'Rovman Powell',
        'team_name': 'Delhi Capitals',
        'user_team_name': 'Shiv, Aryaman',
        'points_row': 38,
        'bidding_row': 55,
    },
    {
        'name': 'Vicky Ostwal',
        'team_name': 'Delhi Capitals',
        'user_team_name': None,
        'points_row': 53,
        'bidding_row': 159,
    },
]
TEAM_CONFIGS = [
    {
        'name': 'Chennai Super Kings',
        'abbrev': 'CSK'
    },
    {
        'name': 'Delhi Capitals',
        'abbrev': 'DC'
    },
    {
        'name': 'Gujarat Titans',
        'abbrev': 'GT'
    },
    {
        'name': 'Kolkata Knight Riders',
        'abbrev': 'KKR'
    },
    {
        'name': 'Punjab Kings',
        'abbrev': 'PK'
    },
    {
        'name': 'Mumbai Indians',
        'abbrev': 'MI'
    },
    {
        'name': 'Sunrisers Hyderabad',
        'abbrev': 'SRH'
    },
    {
        'name': 'Rajasthan Royals',
        'abbrev': 'RR'
    },
    {
        'name': 'Lucknow Super Giants',
        'abbrev': 'LSG'
    },
    {
        'name': 'Royal Challengers Bangalore',
        'abbrev': 'RCB'
    },
]
TOURNAMENT_CONFIG = {
    'series_id': '1298423',
    'channel_id': '996269799539757056',
    'doc_name': 'IPL 15 auction',
}
USER_TEAM_CONFIGS = [
    {
        'name': 'Sardarz',
        'discord_role_id': '998119025773133886',
        'team_points_row': 2,
    },
    {
        'name': 'Neel, Shef, Shikhar',
        'discord_role_id': '1000258844053749812',
        'team_points_row': 3,
    },
    {
        'name': 'Paro, Rahul, Taro',
        'discord_role_id': '1000257644545703987',
        'team_points_row': 4,
    },
    {
        'name': 'Namit',
        'discord_role_id': '998121154969620490',
        'team_points_row': 5,
    },
    {
        'name': 'Ishan, Gayu',
        'discord_role_id': '1000258730899820554',
        'team_points_row': 6,
    },
    {
        'name': 'Desai, Kush, Naman',
        'discord_role_id': '1000258231874113556',
        'team_points_row': 7,
    },
    {
        'name': 'Shiv, Aryaman',
        'discord_role_id': '1000258432890310677',
        'team_points_row': 8,
    },
]


def insert_tournament():
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(Tournament(**TOURNAMENT_CONFIG))


def insert_user_teams():
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects(
            [UserTeam(**config, tournament_id=1) for config in USER_TEAM_CONFIGS]
        )


def insert_teams():
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects([Team(**config, tournament_id=1) for config in TEAM_CONFIGS])


def insert_players():
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in PLAYER_CONFIGS:
            team_id = session.query(Team).filter(Team.name == config['team_name']).first().id
            player = Player(
                name=config['name'],
                team_id=team_id,
                points_row=config['points_row'],
                bidding_row=config['bidding_row'],
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
    insert_tournament()
    insert_user_teams()
    insert_teams()
    insert_players()
    insert_user_team_players()
    insert_matches()
    insert_match_players()
