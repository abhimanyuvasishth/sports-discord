import random
import os

from discord import Embed, Intents
from discord.ext import commands
from dotenv import load_dotenv

from sports_discord import db_utils, sheet_utils
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

    For example: ?shuffle cat,dog,monkey,donkey
    """
    items = ''.join(args).split(',')
    random.shuffle(items)
    await context.reply(', '.join(items))


@bot.command(name='sheet_link')
async def sheet_link(context):
    """
    Returns the link of the google sheet for the tournament

    For example: ?sheet_link
    """
    try:
        tournament = db_utils.get_tournament(context.channel.id)
        sheet = get_sheet(tournament.doc_name, tournament.points_sheet_name)
        embed = Embed(title=tournament.doc_name, url=sheet.spreadsheet.url)
        await context.reply(embed=embed)
    except (IndexError, TypeError):
        await context.reply('bad request')


def get_role_id(roles):
    for role in roles:
        if role.name.startswith('team-'):
            role_id = str(role.id)
            return role_id


@bot.command()
async def info(context):
    """
    Gets information about your team

    For example: ?info
    """
    reply = 'Not a part of any teams for this tournament'
    role_id = get_role_id(context.author.roles)
    if role_id:
        reply = db_utils.get_user_team(role_id)
    await context.reply(reply)


@bot.command()
async def kaptaan(context, *args):
    """
    Sets a kaptaan

    For example: ?kaptaan Kohli
    """
    role_id = get_role_id(context.author.roles)
    player_name = ' '.join(args)
    new_captain = db_utils.get_new_captain(role_id, player_name)

    if len(new_captain) == 0:
        error_message = f"Error: Couldn't find a player on your team with name: '{player_name}'."
        error_message += ' Please choose someone playing in the next match who is on your team.'
        return await context.reply(f'{error_message} ')
    if len(new_captain) > 1:
        names = [candidate[2] for candidate in new_captain]
        error_message = f"""
            Error: Found multiple players with name: '{player_name}', {names}. Please choose one.
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
async def team_points(context):
    """
    Displays team points & ranks

    For example: ?team_points
    """
    num_2_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    message_lines = ['**Team Points**']
    team_points = sheet_utils.get_team_points()
    for team in team_points:
        rank = num_2_words[team['rank'] - 1]
        message_lines.append(f':{rank}: - {team["name"]} with {team["points"]} points')
    await context.reply('\n'.join(message_lines))


bot.run(TOKEN)
