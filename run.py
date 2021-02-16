#!/usr/bin/env python3
import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands
from cogwatch import Watcher

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot= Bot(command_prefix = '!',intents=intents)
bot.remove_command('help')


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
    await bot.process_commands(message)


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    # Instead of mentioning each cog one by one, loop through all python files in directory and add a cog if exists
    bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(TOKEN)


