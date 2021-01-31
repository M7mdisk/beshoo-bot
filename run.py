from inspect import ArgSpec
from itertools import count
import os
import random
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

@bot.command(name="weather",aliases=["طقس"], )
async def weather(ctx,city,lang ='en'):
    if not not bool(set(city) - set(printable)) :
        lang = "ar"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_MAP_KEY}&units=metric&lang={lang}"
    data = requests.get(url).json()
    if data['cod'] != 200:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name=f"Error!", value=f"We could not find that city!", inline=False)
        return await ctx.send(embed=embed)        
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
    await ctx.send(embed=embed)

player1 = ""
player2 = ""
turn = ""
gameOver = True
board = []
winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
@bot.command()
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        #print the board

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("it is <@" + str(player1.id) +">'s turn")
        elif num == 2:
            turn = player2
            await ctx.send("it is <@" + str(player2.id) +">'s turn")
    else:
        await ctx.send("The game is already in progress! Finish it before starting a new one")

@bot.command()
async def place(ctx, pos : int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send(mark + "wins")
                elif count >= 9:
                    await ctx.send("it's a tie!")
                
                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
                
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9, and unmarked tile.")
        else:
            await ctx.send("It's not your turn.")
    else:
        await ctx.send("start a new game, using !tictactoe command")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, Command.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, command.BadArgument):
        await ctx.send("Please make sure to mention/oing players.")

@place.error
async def place_error(ctx, error):
    if isinstance(error, Command.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, command.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

"""
 play command

"""
@bot.command(name = "play")
async def play(ctx, url:str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voiceChannel.connect()

bot.run(TOKEN)
