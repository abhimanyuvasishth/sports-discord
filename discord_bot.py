import os

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

from sports_discord.db_utils import get_tournament, get_user_team
from sports_discord.google_sheet import get_sheet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='/auctionbot')


@bot.command(name='?help')
async def help(context):
    command_examples = '\n'.join([
        '?transfer {in} for {out}',
        '?sheetlink',
    ])
    message = f"Here are examples of valid commands:\n>>> {command_examples}"
    await context.reply(message)


@bot.command(name='?sheetlink')
async def sheet_link(context):
    try:
        tournament = get_tournament(context.channel.id)
        sheet = get_sheet(tournament.doc_name, tournament.points_sheet_name)
        embed = Embed(title=tournament.doc_name, url=sheet.spreadsheet.url)
        await context.reply(embed=embed)
    except (IndexError, TypeError):
        await context.reply('bad request')


@bot.command(name='?info')
async def info(context):
    channel_name = context.channel.name
    reply = f'Not a part of any roles for this tournament (e.g. {context.channel.name}-)'
    for role in context.author.roles:
        if role.name.startswith(channel_name):
            user_team = get_user_team(role.id)
            reply = user_team
    await context.reply(reply)


bot.run(TOKEN)
