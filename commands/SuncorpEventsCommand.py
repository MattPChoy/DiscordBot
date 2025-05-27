from discord.ext import commands
from scrapers.SuncorpGameSchedule import get_suncorp_events


class SuncorpEventsCommand(commands.Cog):
    @commands.hybrid_command(name="suncorp-events")
    async def __suncorp_events__(self, ctx, n_days=3):
        events=get_suncorp_events(n_days)
        await self.send_suncorp_events(ctx, events, n_days)


    @staticmethod
    async def send_suncorp_events(ctx, events, n_days=3):
        message = f"# Suncorp events in the next {n_days} days:\n" if n_days != 1 else "# Suncorp events today:\n"

        for event in events:
            print(event.date)
            event_date = f"📅 {event.date.strftime('%a %d %b')}"
            event_time = ""

            if event.startTime:
                event_time = f"⏰ {event.startTime.strftime('%I:%M %p')}"
            message += f"{event.title} {event_date} {event_time}\n"

        await ctx.send(message)

    @staticmethod
    async def daily_message(channel):
        events = get_suncorp_events(1)

        if len(events) == 0:
            return

        await SuncorpEventsCommand.send_suncorp_events(channel, events, 1)