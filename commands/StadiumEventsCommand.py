from discord.ext import commands
from scrapers.StadiumEventSchedule import get_events
from datetime import datetime

class SuncorpEventsCommand(commands.Cog):
    @commands.hybrid_command(name="events")
    async def __stadium_events__(self, ctx, n_days=3):
        events=get_events(n_days)
        await self.send_stadium_events(ctx, events, n_days)


    @staticmethod
    async def send_stadium_events(ctx, events, n_days=3):
        
        def get_message(events, n_days):
            suncorp_icon = ":sun_with_face:"
            gabba_icon = "🐑"

            message = f"# Stadium events in the next {n_days} days:\n" if n_days != 1 else "# Stadiums events today:\n"
            message += f"{suncorp_icon}: Suncorp, {gabba_icon}: Gabba\n\n"

            
            for event in events:
                event_symbol = suncorp_icon if event.location == 'Suncorp' else gabba_icon
                if event.startTime:
                    epoc_time = str(int(datetime.combine(event.date.date(), event.startTime.time()).timestamp()))
                else:
                    epoc_time = str(int(event.date.timestamp()))
                    
                event_date = f"📅 <t:{epoc_time}:D>"
                event_time = f"<t:{epoc_time}:t>" if event.startTime else ""
                remaining = f"(<t:{epoc_time}:R>)"
                message += f"{event_symbol} {event.title} {event_date} {event_time} {remaining}\n"
            return message
        
        message = get_message(events, n_days)
        await ctx.send(message)

    @staticmethod
    async def daily_message(channel):
        events = get_events(1)

        if len(events) == 0:
            return

        await SuncorpEventsCommand.send_stadium_events(channel, events, 1)