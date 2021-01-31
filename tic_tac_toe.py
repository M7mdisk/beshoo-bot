from itertools import count
import os
import random
import discord
from discord.ext.commands.core import Command, command
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()  
intents.members = True
bot= Bot(command_prefix = '!',intents=intents)

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