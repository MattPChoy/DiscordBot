import discord
from discord.ext import commands
import datetime
from datetime import datetime, UTC, timedelta

from config import dbConnectionString
from data.VoiceChatRepository import VoiceSessionRepository
from util import format_seconds_to_hms


class VCStats(commands.Cog):
    def __init__(self):
        self.voiceRepo = VoiceSessionRepository(dbConnectionString)

    @commands.command(name="vc-stats", brief="Get stats about a user' time in vc")
    async def get_self_vcstats(self, ctx: commands.Context, user: discord.Member = None, n_days: str = "7"):
        user = user or ctx.author  # default to the command invoker

        try:
            days_int = int(n_days)
        except ValueError:
            await ctx.send(f"{n_days} is not a valid number between 1 and 100")
            return

        if not (0 <= days_int <= 100):
            await ctx.send(f"{n_days} is not a valid number between 1 and 100")
            return

        epoch_duration = datetime.now(UTC) - timedelta(days=days_int)
        elapsed = self.voiceRepo.get_vc_time_elapsed(str(user.id), epoch_duration)

        await ctx.send(f"{user.mention} has been in voice chat for {format_seconds_to_hms(elapsed)} over the past {days_int} days.")
