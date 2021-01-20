# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


def handle_command(command,args):
    if command.lower() == "echo":
        return args


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} has connected to the following Guild:\n'
        f"{guild.name}(id: {guild.id})"
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == '!':
        command,args = message.content[1:].split(" ",1)
        print(command,args)
        response = handle_command(command,args)
        await message.channel.send(response)

client.run(TOKEN)
