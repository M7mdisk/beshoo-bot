#!/usr/bin/env python3
import os
import discord
import requests
import json
from dotenv import load_dotenv
from discord.ext.commands import Bot,when_mentioned_or
from discord.ext import commands
from cogwatch import Watcher
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True

def when_mentioned_or_function(func):
    def inner(bot, message):
        r = func(bot, message)
        r = commands.when_mentioned(bot, message) + [r]
        return r
    return inner

def get_prefix(bot, message):
    guild = message.guild
    if not guild:
        return "!"
    r = requests.get(f"https://beshoo-188b1-default-rtdb.firebaseio.com/Servers/{str(message.guild.id)}.json").json()
    if r == None:
        prefix = "!"
        requests.patch(f"https://beshoo-188b1-default-rtdb.firebaseio.com/Servers.json",json.dumps({str(message.guild.id): "!"}))
    else:
        prefix = r
    return prefix 

bot= Bot(command_prefix = when_mentioned_or_function(get_prefix),intents=intents)
bot.remove_command('help')

@bot.event
async def on_guild_join(guild):
    requests.patch(f"https://beshoo-188b1-default-rtdb.firebaseio.com/Servers.json",json.dumps({str(guild.id): "!"}))

@bot.command()
@commands.guild_only()
async def setprefix(ctx, prefix):
    requests.patch(f"https://beshoo-188b1-default-rtdb.firebaseio.com/Servers.json",json.dumps({str(ctx.guild.id): f"{prefix}"}))
    await ctx.send(f"prefix changed to: {prefix}")


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my developers struggle :)"))
    # Watcher for changes in any files in the 'cogs' directory, If anything changes the bot reloads automatically!
    watcher = Watcher(bot, path='cogs')
    await watcher.start()

@bot.event
async def on_command_error(ctx,error):
    # TODO: Add more isinstance statments for better error feedback.
    if isinstance(error,commands.NoPrivateMessage):
        await ctx.send("This command can only be used in a server!")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command. use !help for a list of commands")
    else:
        print(error,error.__cause__)
        

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and 'prefix' in message.content:
        return await message.channel.send( f'My Prefix on this server is {get_prefix(bot,message)}')
    await bot.process_commands(message)


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    # Instead of mentioning each cog one by one, loop through all python files in directory and add a cog if exists
    bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(TOKEN)


