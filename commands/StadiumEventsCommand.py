from discord.ext import commands
from scrapers.StadiumEventSchedule import get_events
import datetime

class SuncorpEventsCommand(commands.Cog):
    @commands.hybrid_command(name="events")
    async def __stadium_events__(self, ctx, n_days:str="3", venue=""):

        try :
            days = int(n_days)
        except ValueError:
            await ctx.reply(f"\"{n_days}\" is not a valid number of days.")
            return
        
        MAX_DAYS = (datetime.date.max - datetime.date.today()).days

        if days > MAX_DAYS:
            await ctx.reply(f"number of days must be less than {MAX_DAYS}")
            return

        if days < 1:
            await ctx.reply("Are you a time traveller?")
            return

        events=get_events(days)
        await self.send_stadium_events(ctx, events, days, venue)

    @staticmethod
    async def send_stadium_events(ctx, events, n_days, venue=""):
        suncorp_icon = ":sun_with_face:"
        gabba_icon = "🏟"

        message = f"# Stadium events in the next {n_days} days:\n" if n_days != 1 else "# Stadiums events today:\n"
        message += f"{suncorp_icon}: Suncorp, {gabba_icon}: Gabba\n\n"

        for event in events:
            if venue.lower() in ["suncorp", "gabba"]:
                if event.location.lower() != venue.lower():
                    continue
            event_symbol = suncorp_icon if event.location == 'Suncorp' else gabba_icon
            event_date = f"📅 {event.date.strftime('%a %d %b')}"
            event_time = ""

            if event.startTime:
                event_time = f"⏰ {event.startTime.strftime('%I:%M %p')}"
            message += f"{event_symbol} {event.title} {event_date} {event_time}\n"

        await ctx.send(message)

    async def daily_message(self, channel):
        events = get_events(1)

        if len(events) == 0:
            return

        await SuncorpEventsCommand.send_stadium_events(channel, events, "1")
