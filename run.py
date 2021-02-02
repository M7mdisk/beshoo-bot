#!/usr/bin/env python3
from inspect import ArgSpec
import os
import platform
import random
from tokenize import Name
import youtube_dl
from youtube_dl import YoutubeDL
from requests import get
from string import printable                                                                                                                                                                           
import discord
from discord import FFmpegPCMAudio
from discord import utils
from discord import client
from discord import channel
from discord import message
from discord.channel import VoiceChannel
from discord.ext.commands.core import Command, command
from dotenv import load_dotenv
from discord.ext.commands import Bot
from time import sleep
import requests
from ttt import TicTacToe
from jpp import VoiceChannels
from admin import Administration

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
            for _ in range(num):
                sleep(0.2)
                await ctx.send(f"{str(user.mention)}, عم اجرب صوتيييي")


@bot.command(name="advice")
async def advice(ctx):
    r = requests.get("https://api.adviceslip.com/advice")
    data = r.json()
    await (data["slip"]["advice"])


@bot.command(name="def")
async def urban(ctx, word):
    data= requests.get(f"http://api.urbandictionary.com/v0/define?term={word}").json()
    top = data['list'][0]
    definition=f"{top['definition'].replace('[','').replace(']','')}"
    e = discord.Embed(title=f"{word.title()}",
            description=definition, color=0x00ff00)
    await ctx.send(embed=e)



@bot.command(name="meme")
async def meme(ctx):
    r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
    data = r.json()
    e = discord.Embed()
    e.set_image(url=data["url"])
    await ctx.send(embed=e)


@bot.command(name = "editme")
async def edit_me(ctx):
  message = await ctx.send("hello")
  await message.edit(content="bye!")


@bot.command(name="weather",aliases=["طقس"], )
async def weather(ctx,city,lang ='en'):
    if not not bool(set(city) - set(printable)) :
        lang = "ar"
    msg = await ctx.send("Measuring...")    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_MAP_KEY}&units=metric&lang={lang}"
    data = requests.get(url).json()
    if data['cod'] != 200:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name=f"Error!", value=f"We could not find that city!", inline=False)
        return await msg.edit(content="",embed=embed)   
    city = data["name"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]
    country = data["sys"]["country"].lower()
    if lang == "ar": 
        embed=discord.Embed(color=0xffffff)
        embed.add_field(name=f":flag_{country}: {city}", value=f"{temp}° س", inline=False)
        embed.add_field(name="كأنها", value=f"{feels_like}° س", inline=True)
        embed.add_field(name="الوصف", value=desc, inline=True)
        embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")
        return await ctx.send(embed=embed)

    embed=discord.Embed(color=0xffffff)
    embed.add_field(name=f":flag_{country}: {city}", value=f"{temp}° c", inline=False)
    embed.add_field(name="Description", value=desc, inline=True)
    embed.add_field(name="Feels Like", value=f"{feels_like}° c", inline=True)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")
    
    return await msg.edit(content="",embed=embed)



@bot.command()
async def ping(ctx):
    stream = os.popen("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
    temp = stream.read()
    embed=discord.Embed(title="Pong!", color=0x00ff1e)
    embed.add_field(name="Latency", value=f"{round(bot.latency,1)}ms", inline=False)
    if platform.system() == "Linux":
        embed.add_field(name="Temperature", value=f"{temp[:-1]}°c", inline=True)
    await ctx.send(embed=embed)

bot.add_cog(TicTacToe(bot))
bot.add_cog(Administration(bot))
bot.add_cog(VoiceChannels(bot))

bot.run(TOKEN)