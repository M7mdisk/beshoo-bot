import os
from os import name
import shlex
from shlex import join
import youtube_dl
from youtube_dl import YoutubeDL
import discord
from discord.ext import commands
from discord.ext.commands import cog
import random
from itertools import count

class VoiceChannels(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.chnl = None
        self.voice = None
        self.ydl_opts = {}
        self.song_there = None
        self.after= None
        self.nname = None

    @commands.command(name = "join")
    @commands.guild_only()
    async def join(self, ctx):
        ''' Join the voice channel '''
        self.chnl = ctx.author.voice.channel
        await self.chnl.connect()
        await ctx.send("I Joined the Voice channel!")

    @commands.command(name = "play")
    @commands.guild_only()
    async def play(self, ctx, url: str):
        ''' Download the URL and play the music '''

        self.song_there = os.path.isfile("song.mp3")
        try:
            if self.song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Getting everything ready now")

        self.voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        self.voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = 0.07

        self.nname = Name.rsplit("-", 2)
        await ctx.send(f"Playing: {self.nname[0]}")
        print("playing\n")

    @commands.command(name = "leave")
    @commands.guild_only()
    async def leave(self, ctx):
        ''' Leave the voice channel '''
        await ctx.voice_client.disconnect()
        await ctx.send("I left the Voice channel!")
