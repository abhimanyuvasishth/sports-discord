import sqlite3

query = """
    INSERT INTO tournament (
        series_id,
        discord_channel_id,
        doc_name,
        points_sheet_name,
        bidding_sheet_name,
        team_points_sheet_name
    )
    VALUES (
        '1298423',
        '996269799539757056',
        'IPL 15 auction',
        'Points Worksheet',
        'Bidding Page',
        'Team Points'
    );
"""


def insert_rows():
    with sqlite3.connect('sports_discord.db') as conn:
        conn.execute(query)
        conn.commit()


def fetch_data(discord_channel_id):
    query = """
        SELECT doc_name, team_points_sheet_name
        FROM tournament
        WHERE discord_channel_id = :discord_channel_id
    """
    with sqlite3.connect('sports_discord.db') as conn:
        cursor = conn.execute(query, {'discord_channel_id': discord_channel_id})
        return cursor.fetchall()


if __name__ == '__main__':
    insert_rows()
