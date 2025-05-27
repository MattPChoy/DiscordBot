from discord.ext import commands
from scrapers.StadiumEventSchedule import get_suncorp_events


class SuncorpEventsCommand(commands.Cog):
    @commands.hybrid_command(name="events")
    async def __stadium_events__(self, ctx, n_days=3):
        events=get_suncorp_events(n_days)
        await self.send_stadium_events(ctx, events, n_days)


    @staticmethod
    async def send_stadium_events(ctx, events, n_days=3):
        suncorp_icon = ":sun_with_face:"
        gabba_icon = "🐑"

        message = f"# Stadium events in the next {n_days} days:\n" if n_days != 1 else "# Stadiums events today:\n"
        message += f"{suncorp_icon}: Suncorp, {gabba_icon}: Gabba\n\n"

        for event in events:
            print(event.date)
            event_symbol = suncorp_icon if event.location == 'Suncorp' else gabba_icon
            event_date = f"📅 {event.date.strftime('%a %d %b')}"
            event_time = ""

            if event.startTime:
                event_time = f"⏰ {event.startTime.strftime('%I:%M %p')}"
            message += f"{event_symbol} {event.title} {event_date} {event_time}\n"

        await ctx.send(message)

    @staticmethod
    async def daily_message(channel):
        events = get_suncorp_events(1)

        if len(events) == 0:
            return

        await SuncorpEventsCommand.send_stadium_events(channel, events, 1)