#libarires
import discord
import configparser
from discord.ext.commands import Bot

#load configuration from .ini file
parser = configparser.ConfigParser()
parser.read('config.ini')

#initalize bot and load extensions
bot = Bot(parser.get('BOT', 'prefix'))
bot.load_extension("cogs.redis")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.gifs")
bot.load_extension("cogs.voting")

#start bot
bot.run(parser.get('BOT', 'token'))

async def UpdateUserNick(m, newNick):
    await m.edit(nick = newNick)
