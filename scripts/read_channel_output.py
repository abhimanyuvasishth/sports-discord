import csv
import os

import discord

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

team_name_mapping = {
    'Shashank Redemption': 'Sri Sri Nataraj Begum',
    'Vande Markram': 'Sri Sri Nataraj Begum',
}


def parse_team_points(points_message):
    lines = points_message.strip().split('\n')
    team_points = {}
    for line in lines[1:]:
        if ' with ' in line:
            parts = line.split(' with ')
            team_name = parts[0].split(' - ')[1]
            team_name = team_name_mapping.get(team_name, team_name)
            points = int(float(parts[1].split(' ')[0]))
            team_points[team_name] = points
        else:
            parts = line.split(': ')
            team_name = parts[1].rsplit(':', 1)[0]
            team_name = team_name_mapping.get(team_name, team_name)
            points = int(float(parts[2].split(' ')[0]))
        team_points[team_name] = points
    return team_points


@client.event
async def on_ready():
    channel = client.get_channel(os.getenv('BOT_SPAM_CHANNEL_ID'))
    dates = set()
    rows = []
    async for message in channel.history(limit=10000):
        if message.author.name != 'AuctionBot':
            continue
        if not message.content.startswith('**Team Points**'):
            continue
        message_date = message.created_at.strftime("%Y-%m-%d")
        if message_date < '2024-03-22' or message_date in dates:
            continue
        team_points = parse_team_points(message.content)
        team_points['date'] = message_date
        rows.append(team_points)
        dates.add(message_date)
        print(team_points)

    rows = list(reversed(rows))
    print(rows)
    dates = [entry['date'] for entry in rows]
    team_names = set()
    for entry in rows:
        team_names.update(entry.keys())
    team_names.discard('date')
    team_names = sorted(team_names)
    final_data = [['team_name'] + dates]

    for team in team_names:
        row = [team]
        for entry in rows:
            row.append(entry.get(team, 0))
        final_data.append(row)

    with open('points_race.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(final_data)
    print('completed')


client.run(os.getenv('DISCORD_TOKEN'))
