from sports_discord.models.associations.tournament_auction_team import \
    tournament_auction_team
from sports_discord.models.associations.tournament_playing_team import \
    tournament_playing_team
from sports_discord.models.auction_team import AuctionTeam
from sports_discord.models.playing_team import PlayingTeam
from sports_discord.models.tournament import Tournament
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


def insert_auction_teams():
    auction_configs = [
        {'name': 'Sardarz', 'discord_role_id': '998119025773133886'},
        {'name': 'Paro, Rahul, Taro', 'discord_role_id': '1000257644545703987'},
        {'name': 'Desai, Kush, Naman', 'discord_role_id': '1000258231874113556'},
        {'name': 'Namit', 'discord_role_id': '998121154969620490'},
        {'name': 'Shiv, Aryaman', 'discord_role_id': '1000258432890310677'},
        {'name': 'Ishan, Gayu', 'discord_role_id': '1000258730899820554'},
        {'name': 'Neel, Shef, Shikhar', 'discord_role_id': '1000258844053749812'},
    ]
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.bulk_save_objects([AuctionTeam(name=config['name']) for config in auction_configs])

    with sessionmaker(engine, autocommit=True).begin() as session:
        tournament = session.query(Tournament).filter(Tournament.channel_id == channel_id).first()
        for config in auction_configs:
            team = session.query(AuctionTeam).filter(AuctionTeam.name == config['name']).first()
            params = {
                'tournament_id': tournament.id,
                'auction_team_id': team.id,
                'discord_role_id': config['discord_role_id']
            }
            session.execute(tournament_auction_team.insert(), params=params)


def insert_playing_teams():
    playing_team_configs = [
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
        session.bulk_save_objects([PlayingTeam(**config) for config in playing_team_configs])

    with sessionmaker(engine, autocommit=True).begin() as session:
        tournament = session.query(Tournament).filter(Tournament.channel_id == channel_id).first()
        for config in playing_team_configs:
            team = session.query(PlayingTeam).filter(PlayingTeam.name == config['name']).first()
            params = {
                'tournament_id': tournament.id,
                'playing_team_id': team.id,
            }
            session.execute(tournament_playing_team.insert(), params=params)


def get_data(query):
    with sessionmaker(engine)() as session:
        result = session.execute(query)
        return result.fetchall()


if __name__ == '__main__':
    insert_tournament()
    insert_auction_teams()
    insert_playing_teams()
