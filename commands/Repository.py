from discord.ext import commands


class Repository(commands.Cog):
    @commands.command(name="repository", brief="Get the bot's source code.")
    async def get_repository(self, ctx):
        await ctx.send(f"My source code can be found at https://github.com/MattPChoy/DiscordBot")