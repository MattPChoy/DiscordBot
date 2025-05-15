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

async def setup_bot():
	await bot.add_cog(Uptime())

import asyncio
asyncio.run(setup_bot())
bot.run(token)