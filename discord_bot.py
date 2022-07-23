import os

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import select

from scripts.insert_data import get_data
from sports_discord.google_sheet import get_sheet
from sports_discord.models.tournament import Tournament

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
        statement = select(Tournament).where(Tournament.channel_id == context.channel.id)
        tournament = get_data(statement)[0][0]
        sheet = get_sheet(tournament.doc_name, tournament.points_sheet_name)
        embed = Embed(title=tournament.doc_name, url=sheet.spreadsheet.url)
        await context.reply(embed=embed)
    except (IndexError, TypeError):
        await context.reply('bad request')

bot.run(TOKEN)
