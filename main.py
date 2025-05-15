import os
import discord
from dotenv import load_dotenv
from commands.Uptime import Uptime 
from discord.ext import commands

load_dotenv()
token = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    channel_id = 1167760258215714817  # Replace with your channel ID
    channel = bot.get_channel(channel_id)
    if channel:
        with open('./assets/anya.gif', 'rb') as f:
            await channel.send(file=discord.File(f, 'anya.gif'))

async def setup_bot():
	await bot.add_cog(Uptime())

import asyncio
asyncio.run(setup_bot())
bot.run(token)