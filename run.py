from inspect import ArgSpec
from itertools import count
import os
import random
import requests
from tic_tac_toe import tictactoe
from weather_ import weather
from string import printable                                                                                                                                                                           
import discord
from discord import utils
from discord import client
from discord.channel import VoiceChannel
from discord.ext.commands.core import Command, command
from dotenv import load_dotenv
from discord.ext.commands import Bot
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()  
intents.members = True
bot= Bot(command_prefix = '!',intents=intents)
OPEN_WEATHER_MAP_KEY = "ea073e04bc85f31dab1408ad497f277f"

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = ': People coding!!'))

@bot.command(name = "server")
async def server_info(context):
    guild = context.guild
    await context.send(f"server name: {guild.name}\nserver size:{len(guild.members)}\nOwner: {guild.owner.display_name}")

@bot.event
async def on_message2(message):
    if message.content == "test":
        await message.channel.send("Testing 1 .. 2 .. 3!")

@bot.command()
async def echo(ctx, *args):
    await ctx.send(' '.join(args))

@bot.command()
async def annoy(ctx,user: discord.Member = None,num = 10):
    if user:
        if user.id == 787194682354040833:
            await ctx.send("No hahahahaahaaaaaaaaa get siked")
        else:
            for i in range(num):
                sleep(0.2)
                await ctx.send(f"{str(user.mention)}, عم اجرب صوتيييي")
        
@bot.command()
async def advice(ctx):
    r = requests.get("https://api.adviceslip.com/advice")
    data = r.json()
    await ctx.send(data["slip"]["advice"])

# @bot.command()
# async def meme(ctx):
#     r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
#     data = r.json()
#     await ctx.send(data["url"])

@bot.command()
async def meme(ctx):
    r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
    data = r.json()
    e = discord.Embed()
    e.set_image(url=data["url"])
    await ctx.send(embed=e)

@bot.command(name="def")
async def urban(ctx, word):
    data= requests.get(f"http://api.urbandictionary.com/v0/define?term={word}").json()
    top = data['list'][0]
    definition=f"{top['definition'].replace('[','').replace(']','')}"
    e = discord.Embed(title=f"{word.title()}",
            description=definition, color=0x00ff00)
    await ctx.send(embed=e)
"""
 play command

"""
@bot.command(name = "play")
async def play(ctx, url:str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voiceChannel.connect()

bot.run(TOKEN)
