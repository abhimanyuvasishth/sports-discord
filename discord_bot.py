import os
import random

import emoji
from discord import Embed, Intents
from discord.ext import commands
from dotenv import load_dotenv

from sports_discord import db_utils, sheet_utils, utils
from sports_discord.constants import (CHANNEL_ID, DOC_NAME, NOT_ON_A_TEAM,
                                      NUMBER_OF_FIELDS, POINTS_SHEET_NAME,
                                      SheetCols)
from sports_discord.google_sheet import get_sheet
from sports_discord.haiku import get_haiku

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents(
    messages=True,
    message_content=True,
    guilds=True
)
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


@bot.command()
async def shuffle(context, *args):
    """
    Shuffles a list of comma separated values

    For example: !shuffle cat,dog,monkey,donkey
    """
    items = ''.join(args).split(',')
    random.shuffle(items)
    await context.reply(', '.join(items))


@bot.command(name='sheet_link')
async def sheet_link(context):
    """
    Returns the link to the google sheet

    For example: !sheet_link
    """
    sheet = get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    embed = Embed(title=DOC_NAME, url=sheet.spreadsheet.url)
    await context.reply(embed=embed)


@bot.command()
async def info(context):
    """
    Gets information about your team

    For example: !info
    """
    role_id = utils.get_role_id(context.author.roles)
    reply = db_utils.get_user_team_by_id(role_id) if role_id else NOT_ON_A_TEAM
    await context.reply(reply)


@bot.command()
async def kaptaan(context, *args):
    """
    Sets a kaptaan

    For example: !kaptaan Kohli
    """
    if context.channel.id != CHANNEL_ID:
        return await context.reply('Please set kaptaan on the main channel for this tournament')

    role_id = utils.get_role_id(context.author.roles)
    if not role_id:
        return await context.reply(NOT_ON_A_TEAM)

    player_name = emoji.demojize(' '.join(args)).replace(':', '')
    new_captain = db_utils.get_new_captain(role_id, player_name)

    if len(new_captain) == 0:
        error_message = f"Error: Couldn't find a player on your team with name: '{player_name}'"
        error_message += ' Please pick someone playing in the next matchday who is on your team.'
        return await context.reply(f'{error_message} ')
    if len(new_captain) > 1:
        names = [candidate[2] for candidate in new_captain][:10]
        error_message = f"""
            Error: Found multiple players with name: '{player_name}' such as {names}
        """
        return await context.reply(error_message)

    new_captain_match_player_id, new_captain_match_num, new_captain_name = new_captain[0]
    message = f'Kaptaan set to {new_captain_name}'

    old_captain = db_utils.get_old_captain(role_id)
    if old_captain:
        old_captain_match_player_id, old_captain_match_num, old_captain_name = old_captain
        db_utils.update_captain(old_captain_match_player_id, False)
        sheet_utils.update_captain(old_captain_name, old_captain_match_num, False)
        message = f'Kaptaan changed from {old_captain_name} to {new_captain_name}'

    db_utils.update_captain(new_captain_match_player_id, True)
    sheet_utils.update_captain(new_captain_name, new_captain_match_num, True)

    await context.reply(message)


@bot.command()
async def points(context, *args):
    """
    Checks a player's total points (kaptaan and non kaptaan) and points in their most recent game

    For example: !points Kohli
    """
    raw_player_name = emoji.demojize(' '.join(args)).replace(':', '')
    player = db_utils.get_player_owner(raw_player_name)

    if len(player) == 0:
        error_message = f"Error: Couldn't find a player with name: '{raw_player_name}'"
        return await context.reply(f'{error_message} ')
    if len(player) > 1:
        names = [candidate[1].name for candidate in player][:10]
        error_message = f"""
            Error: Found multiple players with name: '{raw_player_name}' such as {names}
        """
        return await context.reply(error_message)

    team_name, query_player = player[0]

    try:
        match_num, _ = db_utils.get_player_and_most_recent_match(query_player.id)
        recent_points = sheet_utils.get_points_for_match_num(query_player.name, match_num)
        recent_message = f'Points in Most Recent Match: {recent_points} (match {match_num})'
    except TypeError:
        recent_message = f'{query_player.name} has not played any games yet'

    points = sheet_utils.get_points(query_player.name, kaptaan=True)
    non_kaptaan_points = sheet_utils.get_points(query_player.name, kaptaan=False)
    rank, total = sheet_utils.get_rank(points)
    rating_emoji = utils.get_rating_emoji(rank, total)
    message = [
        f'{query_player}',
        f'Total Points: {points}',
        f'Non Kaptaan Points: {non_kaptaan_points}',
        recent_message,
        f'Rank: {rank} of {total}, overall rating: {rating_emoji}',
        f'Owner: {team_name or "no one"}',
    ]
    await context.reply('\n'.join(message))


@bot.command()
async def haiku(context, *args):
    """
    Generate a haiku for a player

    For example: !haiku Kohli
    """
    raw_player_name = emoji.demojize(' '.join(args)).replace(':', '')
    player_owned = db_utils.get_player_owner(raw_player_name)

    if len(player_owned) == 0:
        error_message = f"Error: Couldn't find a player with name: '{raw_player_name}'"
        return await context.reply(f'{error_message} ')
    if len(player_owned) > 1:
        names = [candidate[1].name for candidate in player_owned][:10]
        error_message = f"""
            Error: Found multiple players with name: '{raw_player_name}' such as {names}
        """
        return await context.reply(error_message)

    _, query_player = player_owned[0]
    haiku = get_haiku(query_player.name)
    message = f"Here's a haiku about {query_player.name}\n{haiku.strip()}"
    await context.reply(message)


@bot.command()
async def team_points(context):
    """
    Displays team points & ranks

    For example: !team_points
    """
    message_lines = ['**Team Points**']
    team_points = sheet_utils.get_team_points()
    for team in team_points:
        emoji = utils.get_emoji_from_number(team['rank'])
        message_lines.append(f'{emoji} {team["name"]}: {team["points"]} points')
    await context.reply('\n'.join(message_lines))


@bot.command()
async def top(context, *args):
    """
    Displays top 10 players and their points, optionally add 'raw' to show non kaptaan points

    For example: !top
    or for non-kaptaan points: !top raw
    """
    message_lines = ['**:fire: Top 10 Players :fire: **']
    raw = ''.join(args).lower() == 'raw'
    for i, row in enumerate(sheet_utils.get_sorted_players(num_players=10, reverse=True, raw=raw)):
        rank_emoji = utils.get_emoji_from_number(i + 1)
        owner = row[SheetCols.POINTS_OWNER_COL.value] or 'no one'
        name = row[SheetCols.NAME_COL.value]
        points_col = SheetCols.RAW_POINTS_COL if raw else SheetCols.POINTS_COL
        points = row[points_col.value - 1]
        message_lines.append(f'{rank_emoji} - {name} with {points} points ({owner})')
    await context.reply('\n'.join(message_lines))


@bot.command()
async def day_points(context):
    """
    Displays team points for the day

    For example: !day_points
    """
    message_lines = ['**:calendar: Today\'s Points :calendar:**']
    player_rows = sheet_utils.get_player_rows()
    player_mapping = {}
    player_db_rows = db_utils.get_all_players_today()
    for row in player_db_rows:
        player_mapping[row[3]] = {
            'match_num': row[0],
            'captain': row[1],
            'team': row[2],
            'points': 0,
        }
    for row in player_rows:
        if not row:
            continue
        mapping = player_mapping.get(row[0])
        if not mapping:
            continue
        col = SheetCols.POINTS_COL.value + NUMBER_OF_FIELDS * mapping['match_num'] - 1
        mapping['points'] = float(row[col])

    team_players = {}
    for name, mapping in player_mapping.items():
        team_name = mapping['team']
        if team_name not in team_players:
            team_players[team_name] = [0, []]
        team_players[team_name][0] += mapping['points']
        if mapping['captain']:
            name += ' (c)'
        team_players[team_name][1].append(f"{name}: {mapping['points']}")

    team_players = dict(sorted(team_players.items(), key=lambda item: item[1][0], reverse=True))
    i = 1
    for team_name, data in team_players.items():
        emoji = utils.get_emoji_from_number(i)
        message_lines.append(f"{emoji} {team_name}: {data[0]} points ({', '.join(data[1])})")
        i += 1

    await context.reply('\n'.join(message_lines))


@bot.command()
async def bottom(context, *args):
    """
    Displays bottom 10 players and their points, optionally add 'raw' to show non kaptaan points

    For example: !bottom
    or for non-kaptaan points: !bottom raw
    """
    message_lines = ['**:lemon: Bottom 10 Players :lemon:**']
    raw = ''.join(args).lower() == 'raw'
    for i, row in enumerate(sheet_utils.get_sorted_players(num_players=10, reverse=False, raw=raw)):
        rank_emoji = utils.get_emoji_from_number(i + 1)
        owner = row[SheetCols.POINTS_OWNER_COL.value] or 'no one'
        name = row[SheetCols.NAME_COL.value]
        points_col = SheetCols.RAW_POINTS_COL if raw else SheetCols.POINTS_COL
        points = row[points_col.value - 1]
        message_lines.append(f'{rank_emoji} - {name} with {points} points ({owner})')
    await context.reply('\n'.join(message_lines))


@bot.command()
async def nickname(context, *args):
    """
    Sets or updates a nickname for one of your players

    For example: !nickname Kohli as the goat
    """
    role_id = utils.get_role_id(context.author.roles)
    if not role_id:
        return await context.reply(NOT_ON_A_TEAM)

    args = list(args)
    if 'as' not in args:
        return await context.reply("Please use `as` to separate name and nickname")

    split_index = args.index('as')
    player_name_raw = ' '.join(args[:split_index])
    nickname_raw = ' '.join(args[split_index + 1:])

    if not player_name_raw or not nickname_raw:
        return await context.reply("Missing player name or nickname")

    player_name = emoji.demojize(player_name_raw).replace(':', '')
    nickname = emoji.demojize(nickname_raw)

    players = db_utils.get_player_out(player_name, role_id)
    if len(players) == 0:
        return await context.reply(f"Couldn't find a player on your team named: '{player_name}'")
    if len(players) > 1:
        names = [p.name for p in players][:10]
        return await context.reply(f"Found multiple players matching '{player_name}': {names}")

    player = players[0]
    db_utils.set_player_nickname(player.id, nickname)
    await context.reply(f"Nickname set for {player.name}: {nickname_raw}")


@bot.command()
async def squad(context, *args):
    """
    Displays the entire squad of a particular auction team

    For example: !squad teamname
    """
    user_team_name = emoji.demojize(' '.join(args)).replace(':', '')
    user_team = db_utils.get_user_team_by_name(user_team_name)

    if len(user_team) == 0:
        error_message = f"Error: Couldn't find an auction team with name: '{user_team_name}'"
        return await context.reply(f'{error_message} ')
    if len(user_team) > 1:
        names = [candidate[1] for candidate in user_team]
        error_message = f"""
            Error: Found multiple teams with name: '{user_team_name}' such as {names}
        """
        return await context.reply(error_message)

    user_team_id, user_team_name = user_team[0]
    squad_rows = db_utils.get_squad(user_team_id)
    squad = [str(player) for player in squad_rows]
    message = f"Team {user_team_name}'s Squad: {squad}"
    await context.reply(message)


@bot.command()
async def transfer(context, *args):
    """
    Transfer player in for player out

    For example: !transfer wantthisperson for dontwantthisperson
    """
    if context.channel.id != CHANNEL_ID:
        return await context.reply('Please make transfers on the main channel for this tournament')

    role_id = utils.get_role_id(context.author.roles)
    if not role_id:
        return await context.reply(NOT_ON_A_TEAM)

    all_args = ' '.join(args).lower()
    user_team = db_utils.get_user_team_by_id(role_id)

    if 'for' not in all_args:
        return await context.reply('Error: Try !transfer player_in for player_out')

    player_name_in = all_args.split('for')[0].strip()
    player_name_out = all_args.split('for')[1].strip()
    players_out = db_utils.get_player_out(player_name_out, role_id)

    if len(players_out) == 0:
        error_message = f"Error: Couldn't find a player on your team with name: '{player_name_out}'"
        return await context.reply(f'{error_message} ')
    if len(players_out) > 1:
        names = [candidate.name for candidate in players_out][:10]
        error_message = f"""
            Error: Found multiple players with name: '{player_name_out}' such as {names}
        """
        return await context.reply(error_message)
    player_out = players_out[0]

    players_in = db_utils.get_player_in(player_name_in)
    if len(players_in) == 0:
        error_message = f"Error: Couldn't find an available player with name: '{player_name_in}'"
        return await context.reply(f'{error_message} ')
    if len(players_in) > 1:
        names = [candidate.name for candidate in players_in][:10]
        error_message = f"""
            Error: Found multiple players with name: '{player_name_in}' such as {names}
        """
        return await context.reply(error_message)
    player_in = players_in[0]

    # TODO: Check pool/position logistics

    # Get points
    player_in_points = sheet_utils.get_points(player_in.name, kaptaan=True)
    player_out_points = sheet_utils.get_points(player_out.name, kaptaan=True)
    adjusted_points = player_out_points - player_in_points

    # Update db
    db_utils.update_player_user_team(player_in.id, user_team.id)
    db_utils.update_player_user_team(player_out.id, None)

    # Update bidding page
    sheet_utils.update_owner(player_in.name, user_team.name)
    sheet_utils.update_owner(player_out.name, '', 1)

    # Store points
    sheet_utils.adjust_transfer_points(user_team.name, adjusted_points)

    await context.reply(f'Transfer made, IN={player_in.name} for OUT={player_out.name}')


bot.run(TOKEN)
