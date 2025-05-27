from discord.ext import commands
import datetime

class Uptime(commands.Cog):
    def __init__(self):
        self.start_time = datetime.datetime.now()

    @commands.command()
    async def uptime(self, ctx):
        delta = datetime.datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Uptime: {hours}h {minutes}m {seconds}s")
