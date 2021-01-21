import discord
import asyncio
import os
import random
import datetime
from dotenv import load_dotenv

bot = discord.Client()

@bot.event
async def on_member_join(member):
    if member.id == bot.id:
        return
    channel = discord.utils.get(bot.guilds[0].channels, name="general")
    response = f"Welcome to b-t-s server, {member.name}."
    await channel.send(response)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    keywords = ["work", "workout", "push", "pushup", "up"]
    channel = message.channel
    for keyword in keywords:
        if keyword.lower() in mesage.content.lower():
            response = f"Did someone say {keyword.lower()}? Drop and give me 10 <@{message.channel}"
            await channel.send(response) 

@bot.event
async def pushup_remainder():
    while(True):
        await bot.wait_until_ready()
        online_members = []
        for member in bot.get_all_members():
            if member.status != discord.Status.oofline and member.id != bot.user.id:
                online_members.append(member.id)
        if len(online_members) > 0:
            user = random.choice(online.members)
            current_time = int(datetime.datetime.now().strftime("%I"))
            channel = discord.utils.get(bot.guilds0[0].channels, name="general")
            message = f"It's {current_time} o'clock! Time for some pushups <@{user}>!"
            await channel.send(message)
    await asyncio.sleep(3600)

bot.loop.create_task(pushup_remainder())

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)