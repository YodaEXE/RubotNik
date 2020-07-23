from discord.ext import commands

class Gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.command()
    async def seo(self, ctx):
        await ctx.send('https://imgur.com/a/v1vdtyh')

    @commands.command()
    async def weak(self, ctx):
        await ctx.send('https://imgur.com/rU4l3SV')

    @commands.command()
    async def hex(self, ctx):
        await ctx.send('https://imgur.com/YYAz1hx')

def setup(bot):
    bot.add_cog(Gifs(bot))