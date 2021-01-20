# bot.py
import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


def handle_command(command,args):
    command = command.lower()
    if command == "echo":
        return args

    if command == "flip":
        choices = ["heads","tails"]
        answer = random.choice(choices)
        return f"You got {answer}"


@client.event
async def on_ready():
    # for guild in client.guilds:
    #     if guild.name == GUILD:
    #         break

    print(
        f'{client.user} has connected to the following Guild:\n'
        f"{guild.name}(id: {guild.id})"
    )
    # await message.channel.send("I am online!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content[0] == '!':
        l = message.content[1:].split(" ",1)# !echo asdjklfhsadf ['echo','asdjklfhsadf']
        if len(l) > 1:
            command,args = l 
        else:
            command = l[0]
            args = ""
        print(command,args)
        response = handle_command(command,args)
        await message.channel.send(response)

client.run(TOKEN)
