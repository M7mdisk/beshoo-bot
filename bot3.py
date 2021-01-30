from inspect import ArgSpec
import os
import random
import discord
from discord.ext.commands.core import command
from dotenv import load_dotenv
from discord.ext.commands import Bot
from time import sleep
import requests

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
        if str(user.id) == "787194682354040833":
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

@bot.command()
async def meme(ctx):
    r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
    data = r.json()
    await ctx.send(data["url"])
bot.run(TOKEN)
