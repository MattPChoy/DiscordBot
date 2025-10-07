from discord import Embed
from discord.ext import commands

from config import dbConnectionString
from data.VoiceChatRepository import VoiceSessionRepository
from util import format_seconds_to_hms


class VCLeaderboard(commands.Cog):
    def __init__(self):
        self.voiceRepo = VoiceSessionRepository(dbConnectionString)

    @commands.command(name="vc-leaderboard", brief="Get stats about users' time in vc")
    async def get_vc_leaderboard(self, ctx, n_days: str = "7", top_n: str = "5"):
        try:
            days_int = int(n_days)
        except ValueError:
            await ctx.reply(f"\"{n_days}\" is not a valid number of days.")
            return

        if not (1 <= days_int <= 100):
            await ctx.send(f"{n_days} is not a valid number between 1 and 100")
            return

        try:
            n = int(top_n)
        except ValueError:
            await ctx.reply(f"{top_n} is not a valid number")
            return

        if not (1 <= n <= 20):
            await ctx.send(f"{top_n} must be between 1 and 20")
            return

        stats = self.voiceRepo.get_top_vc_chatters(n, days_int)

        embed = Embed(
            title=f"🏆 Top {n} VC Yappers - Last {days_int} Days",
            color=0x00ff00
        )

        for userStats in stats:
            hms_string = format_seconds_to_hms(userStats.total_seconds)
            embed.add_field(
                name=f"@{userStats.username}",
                value=hms_string,
                inline=False
            )

        await ctx.send(embed=embed)
