import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
bot= commands.Bot(command_prefix = '!')


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = ': People coding!!'))

@bot.event
async def on_message(message):
    if message.content == "test":
        await message.channel.send("Testing 1 .. 2 .. 3!")

@bot.command(name = "server")
async def server_info(context):
    guild = context.guild
    await context.send(f"server name: {guild.name}\n server size: {len(guild.members)}\n Owner: {guild.owner.display_name}")


bot.run(TOKEN)