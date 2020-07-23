from discord.ext import commands
import redis

class RedisClient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        #TODO: Turn this is to a function with try/catch
        self.bot.data = redis.Redis(host='redis', port=6379)

def setup(bot):
    bot.add_cog(RedisClient(bot))