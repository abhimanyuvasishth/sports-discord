from sports_discord.models.auction_team import AuctionTeam
from sports_discord.models.playing_team import PlayingTeam
from sports_discord.models.tournament import Tournament
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    auction_team = {
        'role_id': '998119025773133886',
        'name': 'Sardarz',
        'tournament_id': 1,
    }
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(AuctionTeam(**auction_team))


def insert_playing_teams():
    playing_team = {
        'name': 'Chennai Super Kings',
        'tournament_id': 1,
    }
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(PlayingTeam(**playing_team))


def get_data(query):
    with sessionmaker(engine)() as session:
        result = session.execute(query)
        return result.fetchall()


if __name__ == '__main__':
    # insert_tournament()
    # insert_auction_teams()
    insert_playing_teams()
