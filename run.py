#!/usr/bin/env python3
from inspect import ArgSpec
import os
import random
from tokenize import Name
import youtube_dl
from youtube_dl import YoutubeDL
from requests import get
import discord
from discord import FFmpegPCMAudio, utils, client, channel, message
from discord.channel import VoiceChannel
from discord.ext.commands.core import Command, command
from dotenv import load_dotenv
from discord.ext.commands import Bot
from time import sleep
import requests
from misc import Miscellaneous
from ttt import TicTacToe
from voice import VoiceChannels
from admin import Administration
from Random import random
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot= Bot(command_prefix = '!',intents=intents)


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = ': People coding!!'))

@bot.event
async def on_message2(message):
    if message.content == "test":
        await message.channel.send("Testing 1 .. 2 .. 3!")


bot.add_cog(Miscellaneous(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(Administration(bot))
bot.add_cog(VoiceChannels(bot))
bot.add_cog(random(bot))

bot.run(TOKEN)