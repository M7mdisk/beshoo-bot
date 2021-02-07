#!/usr/bin/env python3
import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands
from cogs.misc import Miscellaneous
from cogs.ttt import TicTacToe
from cogs.voice import VoiceChannels
from cogs.admin import Administration
from cogs.Random import Random
from cogs.images import Images
from cogs.help import HELP
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot= Bot(command_prefix = '!',intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="errors"))


@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.NoPrivateMessage):
        await ctx.send("This command can only be used in a server!")
    else:
        print(error.__cause__)
        
bot.add_cog(Images(bot))
bot.add_cog(Miscellaneous(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(Administration(bot))
bot.add_cog(VoiceChannels(bot))
bot.add_cog(Random(bot))
bot.add_cog(HELP(bot))
bot.run(TOKEN)
