import os

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

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
    sheet = {
        'url': 'https://docs.google.com/spreadsheets/d/1eUcfzx33UQ4Os_xKF74cekiu8CQK9WDEqk6yhzQXlnc/edit#gid=1030497894',
        'title': 'IPL 15 Auction'
    }
    embed = Embed(title=sheet['title'], url=sheet['url'])
    await context.reply(embed=embed)

bot.run(TOKEN)
