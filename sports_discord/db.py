from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sports_discord.tournament import Tournament

engine = create_engine('sqlite:///sports_discord.db')


def insert_rows():
    tournament = {
        'series_id': '1298423',
        'channel_id': '996269799539757056',
        'doc_name': 'IPL 15 auction',
    }
    with sessionmaker(engine, autocommit=True).begin() as session:
        session.add(Tournament(**tournament))


def get_data(query):
    with sessionmaker(engine)() as session:
        result = session.execute(query)
        return result.fetchall()


if __name__ == '__main__':
    insert_rows()
