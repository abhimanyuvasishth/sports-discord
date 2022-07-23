from sports_discord.models.player import Player
from sports_discord.models.team import Team
from sports_discord.models.tournament import Tournament
from sports_discord.models.user_team import UserTeam
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

channel_id = '996269799539757056'
engine = create_engine('sqlite:///sports_discord.db')


def insert_tournament():
    tournament = {
        'series_id': '1298423',
        'channel_id': '996269799539757056',
        'doc_name': 'IPL 15 auction',
    }
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(Tournament(**tournament))


def insert_user_teams():
    configs = [
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
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects([UserTeam(**config, tournament_id=1) for config in configs])


def insert_teams():
    configs = [
        {'name': 'Chennai Super Kings', 'abbrev': 'CSK'},
        {'name': 'Delhi Capitals', 'abbrev': 'DC'},
        {'name': 'Gujarat Titans', 'abbrev': 'GT'},
        {'name': 'Kolkata Knight Riders', 'abbrev': 'KKR'},
        {'name': 'Punjab Kings', 'abbrev': 'PK'},
        {'name': 'Mumbai Indians', 'abbrev': 'MI'},
        {'name': 'Sunrisers Hyderabad', 'abbrev': 'SRH'},
        {'name': 'Rajasthan Royals', 'abbrev': 'RR'},
        {'name': 'Lucknow Super Giants', 'abbrev': 'LSG'},
        {'name': 'Royal Challengers Bangalore', 'abbrev': 'RCB'},
    ]
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects([Team(**config, tournament_id=1) for config in configs])


def insert_players():
    configs = [
        {
            'name': 'Ambati Rayudu',
            'team_name': 'Chennai Super Kings',
            'points_row': 6,
            'bidding_row': 47,
        },
        {
            'name': 'Robin Uthappa',
            'team_name': 'Chennai Super Kings',
            'points_row': 24,
            'bidding_row': 127,
        },
        {
            'name': 'Anrich Nortje',
            'team_name': 'Delhi Capitals',
            'points_row': 34,
            'bidding_row': 51,
        },
        {
            'name': 'Vicky Ostwal',
            'team_name': 'Delhi Capitals',
            'points_row': 53,
            'bidding_row': 159,
        },
    ]
    with sessionmaker(engine, autocommit=True).begin() as session:
        for config in configs:
            team_id = session.query(Team).filter(Team.name == config['team_name']).first().id
            session.add(
                Player(
                    name=config['name'],
                    team_id=team_id,
                    points_row=config['points_row'],
                    bidding_row=config['bidding_row'],
                )
            )


def get_data(query):
    with sessionmaker(engine)() as session:
        result = session.execute(query)
        return result.fetchall()


if __name__ == '__main__':
    insert_tournament()
    insert_user_teams()
    insert_teams()
    insert_players()
