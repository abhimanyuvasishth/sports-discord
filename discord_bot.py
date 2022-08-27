import random
import os

from discord import Embed, Intents
from discord.ext import commands
from dotenv import load_dotenv

from sports_discord.db_utils import get_tournament, get_user_team
from sports_discord.google_sheet import get_sheet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='?', intents=Intents(messages=True, guilds=True))


@bot.command()
async def shuffle(context, args):
    """
    Shuffles a list of comma separated values.

    For example: ?shuffle cat,dog,monkey,donkey
    """
    items = args.split(',')
    random.shuffle(items)
    await context.reply(', '.join(items))


@bot.command(name='sheet_link')
async def sheet_link(context):
    """
    Returns the link of the google sheet for the tournament.

    For example: ?sheet_link
    """
    try:
        tournament = get_tournament(context.channel.id)
        sheet = get_sheet(tournament.doc_name, tournament.points_sheet_name)
        embed = Embed(title=tournament.doc_name, url=sheet.spreadsheet.url)
        await context.reply(embed=embed)
    except (IndexError, TypeError):
        await context.reply('bad request')


@bot.command()
async def info(context):
    """
    Get information about your team.

    For example: ?info
    """
    reply = 'Not a part of any teams for this tournament'
    for role in context.author.roles:
        if role.name.startswith('team-'):
            user_team = get_user_team(str(role.id))
            reply = user_team
    await context.reply(reply)


bot.run(TOKEN)
