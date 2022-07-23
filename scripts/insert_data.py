from sports_discord.models.auction_team import AuctionTeam
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
    tournament = {
        'role_id': '998119025773133886',
        'team_name': 'Sardarz',
        'tournament_id': 1,
    }
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(AuctionTeam(**tournament))


def get_data(query):
    with sessionmaker(engine)() as session:
        result = session.execute(query)
        return result.fetchall()


if __name__ == '__main__':
    # insert_tournament()
    insert_auction_teams()
