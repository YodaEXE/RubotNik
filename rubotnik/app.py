#libarires
import discord
from discord.ext.commands import Bot
import os

#initalize bot with desired prefix and load extensions
bot = Bot(">")
bot.load_extension("cogs.redis")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.gifs")
bot.load_extension("cogs.voting")

#start bot
bot.run(os.environ['TOKEN'])

async def UpdateUserNick(m, newNick):
    await m.edit(nick = newNick)