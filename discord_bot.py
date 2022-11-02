import os
import random

from discord import Embed, Intents
from discord.ext import commands
from dotenv import load_dotenv

from sports_discord import db_utils, sheet_utils
from sports_discord.constants import DOC_NAME, NOT_ON_A_TEAM, POINTS_SHEET_NAME
from sports_discord.google_sheet import get_sheet

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


def get_role_id(roles):
    for role in roles:
        if role.name.startswith('team-'):
            role_id = str(role.id)
            return role_id


@bot.command()
async def info(context):
    """
    Gets information about your team

    For example: !info
    """
    role_id = get_role_id(context.author.roles)
    reply = db_utils.get_user_team_by_id(role_id) if role_id else NOT_ON_A_TEAM
    await context.reply(reply)


@bot.command()
async def kaptaan(context, *args):
    """
    Sets a kaptaan

    For example: !kaptaan Kohli
    """
    role_id = get_role_id(context.author.roles)
    if not role_id:
        return await context.reply(NOT_ON_A_TEAM)

    player_name = ' '.join(args)
    new_captain = db_utils.get_new_captain(role_id, player_name)

    if len(new_captain) == 0:
        error_message = f"Error: Couldn't find a player on your team with name: '{player_name}'"
        error_message += ' Please pick someone playing in the next matchday who is on your team.'
        return await context.reply(f'{error_message} ')
    if len(new_captain) > 1:
        names = [candidate[2] for candidate in new_captain]
        error_message = f"""
            Error: Found multiple players with name: '{player_name}', {names}, please pick one
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
async def whohas(context, *args):
    """
    Checks who owns a player

    For example: !whohas Kohli
    """
    raw_player_name = ' '.join(args)
    player_owned = db_utils.get_player_owner(raw_player_name)

    if len(player_owned) == 0:
        error_message = f"Error: Couldn't find a player with name: '{raw_player_name}'"
        return await context.reply(f'{error_message} ')
    if len(player_owned) > 1:
        names = [candidate[1] for candidate in player_owned]
        error_message = f"""
            Error: Found multiple players with name: '{raw_player_name}', {names}, please pick one
        """
        return await context.reply(error_message)

    team_name, player_name = player_owned[0]
    owner = f'Team {team_name}' if team_name else 'No one'
    message = f'{owner} has {player_name}'
    await context.reply(message)


@bot.command()
async def team_points(context):
    """
    Displays team points & ranks

    For example: !team_points
    """
    num_2_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    message_lines = ['**Team Points**']
    team_points = sheet_utils.get_team_points()
    for team in team_points:
        rank = num_2_words[team['rank'] - 1]
        message_lines.append(f':{rank}: - {team["name"]} with {team["points"]} points')
    await context.reply('\n'.join(message_lines))


@bot.command()
async def squad(context, *args):
    """
    Displays the entire squad of a particular auction team

    For example: !squad teamname
    """
    user_team_name = ' '.join(args)
    user_team = db_utils.get_user_team_by_name(user_team_name)

    if len(user_team) == 0:
        error_message = f"Error: Couldn't find an auction team with name: '{user_team_name}'"
        return await context.reply(f'{error_message} ')
    if len(user_team) > 1:
        names = [candidate[1] for candidate in user_team]
        error_message = f"""
            Error: Found multiple teams with name: '{user_team_name}', {names}, please pick one
        """
        return await context.reply(error_message)

    user_team_id, user_team_name = user_team[0]
    squad_rows = db_utils.get_squad(user_team_id)
    squad = [squad_row[0] for squad_row in squad_rows]
    message = f"Team {user_team_name}'s Squad: {squad}"
    await context.reply(message)


@bot.command()
async def transfer(context, *args):
    """
    Transfer player in for player out

    For example: !transfer wantthisperson for dontwantthisperson
    """
    role_id = get_role_id(context.author.roles)
    if not role_id:
        return await context.reply(NOT_ON_A_TEAM)

    all_args = ' '.join(args).lower()
    user_team = db_utils.get_user_team_by_id(role_id)

    if 'for' not in all_args:
        return await context.reply('Error: Try !transfer player1 for player2')

    player_name_in = all_args.split('for')[0].strip()
    player_name_out = all_args.split('for')[1].strip()
    players_out = db_utils.get_player_out(player_name_out, role_id)

    if len(players_out) == 0:
        error_message = f"Error: Couldn't find a player on your team with name: '{player_name_out}'"
        return await context.reply(f'{error_message} ')
    if len(players_out) > 1:
        names = [candidate.name for candidate in players_out]
        error_message = f"""
            Error: Found multiple players with name: '{player_name_out}', {names}, please pick one
        """
        return await context.reply(error_message)
    player_out = players_out[0]

    players_in = db_utils.get_player_in(player_name_in)
    if len(players_in) == 0:
        error_message = f"Error: Couldn't find an available player with name: '{player_name_in}'"
        return await context.reply(f'{error_message} ')
    if len(players_in) > 1:
        names = [candidate.name for candidate in players_in]
        error_message = f"""
            Error: Found multiple players with name: '{player_name_in}', {names}, please pick one
        """
        return await context.reply(error_message)
    player_in = players_in[0]

    # TODO: Check pool logistics

    # Get points
    player_in_points = sheet_utils.get_points(player_in.name)
    player_out_points = sheet_utils.get_points(player_out.name)
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
