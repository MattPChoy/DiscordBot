import datetime
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from commands import Uptime, Repository
from commands.StadiumEventsCommand import SuncorpEventsCommand
from config import GENERAL_CHANNEL_ID

load_dotenv()
token = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    channel_id = GENERAL_CHANNEL_ID
    channel = bot.get_channel(channel_id)
    morning_update.start()


@tasks.loop(time=datetime.time(hour=9, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=10))))
async def morning_update():
    channel_id = GENERAL_CHANNEL_ID
    channel = bot.get_channel(channel_id)

    if channel is None:
        print("Cannot find the channel with id " + str(channel_id))
        return

    await SuncorpEventsCommand.daily_message(channel)


async def setup_bot():
    await bot.add_cog(Uptime())
    await bot.add_cog(Repository())
    await bot.add_cog(SuncorpEventsCommand())


import asyncio

asyncio.run(setup_bot())
bot.run(token)
