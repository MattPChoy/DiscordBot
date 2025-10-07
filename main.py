import datetime
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from commands import Uptime, Repository
from commands.StadiumEventsCommand import SuncorpEventsCommand
from commands.VCLeaderboard import VCLeaderboard
from commands.VCStats import VCStats
from config import GENERAL_CHANNEL_ID, dbConnectionString, LOGS_CHANNEL_ID
from data.VoiceChatRepository import VoiceSessionRepository

load_dotenv()
token = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

voiceRepo = VoiceSessionRepository(dbConnectionString)

@bot.event
async def on_ready():
    channel_id = GENERAL_CHANNEL_ID
    channel = bot.get_channel(channel_id)
    morning_update.start()

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    log_channel = bot.get_channel(LOGS_CHANNEL_ID)
    prev_channel = None if before.channel == None else before.channel.name
    after_channel = None if after.channel == None else after.channel.name
    if prev_channel == after_channel:
        # At this point we don't care if the channel didn't change
        # This could be e.g. deafen, mute, server mute
        return

    if before.channel is not None:
        voiceRepo.end_session(member, before.channel.name)
        await log_channel.send(
            f"{member.name} left {before.channel.name}"
        )

    if after.channel is not None:
        voiceRepo.start_session(member, after.channel.name)
        await log_channel.send(
            f"{member.name} joined {after.channel.name}"
        )

@tasks.loop(time=datetime.time(hour=9, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=10))))
async def morning_update():
    channel_id = GENERAL_CHANNEL_ID
    channel = bot.get_channel(channel_id)

    if channel is None:
        print("Cannot find the channel with id " + str(channel_id))
        return

    await SuncorpEventsCommand.daily_message(channel)

PIN_EMOJI = "📌"
PIN_THRESHOLD = 2

async def handle_pin_check(payload: discord.RawReactionActionEvent):
    """Check current pin reaction count and pin/unpin accordingly."""
    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return

    try:
        message = await channel.fetch_message(payload.message_id)
    except discord.NotFound:
        return

    # Find the 📌 reaction object
    pin_reaction = discord.utils.get(message.reactions, emoji=PIN_EMOJI)
    if not pin_reaction:
        # All pin reactions removed
        if message.pinned:
            try:
                await message.unpin()
                print(f"Unpinned message {message.id} in #{channel.name} (no reactions left)")
            except discord.Forbidden:
                print("Missing permissions to unpin the message.")
            except discord.HTTPException as e:
                print(f"Failed to unpin message: {e}")
        return

    # Get list of unique users
    users = [user async for user in pin_reaction.users()]
    unique_user_ids = {user.id for user in users if not user.bot}

    if len(unique_user_ids) >= PIN_THRESHOLD:
        if not message.pinned:
            try:
                await message.pin()
                print(f"Pinned message {message.id} in #{channel.name}")
            except discord.Forbidden:
                print("Missing permissions to pin the message.")
            except discord.HTTPException as e:
                print(f"Failed to pin message: {e}")
    else:
        if message.pinned:
            try:
                await message.unpin()
                print(f"Unpinned message {message.id} in #{channel.name} (reaction count dropped)")
            except discord.Forbidden:
                print("Missing permissions to unpin the message.")
            except discord.HTTPException as e:
                print(f"Failed to unpin message: {e}")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) == PIN_EMOJI:
        await handle_pin_check(payload)

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) == PIN_EMOJI:
        await handle_pin_check(payload)

async def setup_bot():
    await bot.add_cog(Uptime())
    await bot.add_cog(Repository())
    await bot.add_cog(SuncorpEventsCommand())
    await bot.add_cog(VCStats())
    await bot.add_cog(VCLeaderboard())


import asyncio

asyncio.run(setup_bot())
bot.run(token)
