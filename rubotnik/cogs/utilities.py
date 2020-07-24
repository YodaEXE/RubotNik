import discord
from discord.ext import commands
import random

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    async def UpdateUserNick(m, newNick):
        await m.edit(nick = newNick)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def topic(self, ctx, *arg):
        #join arguments and load into database if it doesn't exist
        t = ' '.join(str(i) for i in arg)
        if not self.bot.data.sismember("topics",t) and t != "":
            self.bot.data.sadd("topics", t)

        await ctx.channel.edit(topic = t)

    @commands.command()
    async def randtopic(self, ctx):
        topics = self.bot.data.smembers("topics")
        #Topics are a set, to allow CHOICE to work you must set as tuple in parameter and decode returned byte type
        rand_topic = random.choice(tuple(topics)).decode("utf-8") 
        await ctx.channel.edit(topic = rand_topic)

    @commands.command()
    async def randnick(self, ctx):
        usernames = self.bot.data.smembers("users")
        #Usernames are a set, to allow CHOICE to work you must set as tuple in parameter and decode returned byte type
        rand_username = random.choice(tuple(usernames)).decode("utf-8") 
        await ctx.author.edit(nick = rand_username)

    @commands.command()
    async def nick(self, ctx, *arg):
        names = ' '.join(str(i) for i in arg).split("|")

        if len(names) != 2:
            "Incorrect number of entries, please use: !nick oldnick | newNick"
        else:
            #clean up nicks
            old = names[0].strip().lower()
            newNick = names[1].strip()

            #iterate over members looking for nick match
            for m in ctx.channel.members.list:
                if not m.nick == None and m.nick.lower() == old:
                    update_user = m
    
        #If user is not blank, and doesn't exist in DB, add it.
        if update_user != None and not self.bot.data.sismember("users",newNick):
            self.bot.data.sadd("users",newNick)

        await update_user.edit(nick = newNick)

    @commands.command()
    async def nickparty(self, ctx):
        nicks = list(self.bot.data.smembers("users"))
        

        for m in list(ctx.channel.members):
            newNick = random.choice(nicks).decode("utf-8") 

            if m.bot == False and discord.utils.get(m.roles, name="Owner") == None:
                print(f"renaming user: {m.name}")
                await m.edit(nick = newNick)

    @commands.command()
    async def lmgtfy(self, ctx, arg):
        await ctx.send("http://lmgtfy.com/?q="+ cgi.escape(arg))

def setup(bot):
    bot.add_cog(Utilities(bot))