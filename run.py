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
from ttt import TicTacToe
from admin import Administration
from misc import Miscellaneous
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


### new:
@bot.command(name = "join")
async def join(ctx):
    chnl = ctx.author.voice.channel
    await chnl.connect()
    await ctx.send("I Joined the Voice channel!")

### new:
@bot.command(name = "play")
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    #voice = get(bot.voice_clients, ctx.guild)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = Name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

### new:
@bot.command(name = "leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("I left the Voice channel!")


bot.add_cog(TicTacToe(bot))
bot.add_cog(Administration(bot))
bot.add_cog(Miscellaneous(bot))

bot.run(TOKEN)