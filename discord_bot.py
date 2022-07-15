import os

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

from sports_discord.db import fetch_data
from sports_discord.google_sheet import get_sheet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


tournaments = {}
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
        sheet = tournaments[context.channel.id]
    except KeyError:
        doc_name, sheet_name = fetch_data(context.channel.id)[0]
        sheet = get_sheet(doc_name=doc_name, sheet_name=sheet_name)
        tournaments[context.channel.id] = sheet

    embed = Embed(title=sheet.spreadsheet.title, url=sheet.spreadsheet.url)
    await context.reply(embed=embed)

bot.run(TOKEN)
