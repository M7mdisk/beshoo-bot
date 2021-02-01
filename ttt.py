import discord
import random
from discord.ext import commands
from itertools import count

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

class TicTacToe(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.player1 = None
        self.player2 = None
        self.turn = None
        self.gameOver = True
        self.board = []
        self.count = count

    @commands.command()
    async def tictactoe(self, ctx, p1 : discord.Member, p2 : discord.Member):

        if self.gameOver:
            self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            self.turn = ""
            self.gameOver = False
            self.count = 0

            self.player1 = p1
            self.player2 = p2

            #print the self.board

            line = ""
            for x in range(len(self.board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + self.board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + self.board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                self.turn = self.player1
                await ctx.send("it is <@" + str(self.player1.id) +">'s turn")
            elif num == 2:
                self.turn = self.player2
                await ctx.send("it is <@" + str(self.player2.id) +">'s turn")
        else:
            await ctx.send("The game is already in progress! Finish it before starting a new one")

    @commands.command()
    async def place(self,ctx, pos : int):
        if not self.gameOver:
            mark = ""
            if self.turn == ctx.author:
                if self.turn == self.player1:
                    mark = ":regional_indicator_x:"
                elif self.turn == self.player2:
                    mark = ":o2:"
                if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
                    self.board[pos - 1] = mark
                    self.count += 1

                    # print self.board
                    line = ""
                    for x in range(len(self.board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + self.board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + self.board[x]

                    self.checkWinner(winningConditions, mark)
                    if self.gameOver:
                        await ctx.send(mark + "wins")
                    elif self.count >= 9:
                        await ctx.send("it's a tie!")
                    
                    # switch turns
                    if self.turn == self.player1:
                        self.turn = self.player2
                    elif self.turn == self.player2:
                        self.turn = self.player1
                    
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9, and unmarked tile.")
            else:
                await ctx.send("It's not your turn.")
        else:
            await ctx.send("start a new game, using !tictactoe command")

    @commands.command()
    async def endgame(self,ctx):
        self.gameOver = True
        await ctx.send(f"Game between {self.player1.mention} and {self.player2.mention} Ended.")
    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/oing players.")

    @place.error
    async def place_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")

    def checkWinner(self,winningConditions, mark):
        for condition in winningConditions:
            if self.board[condition[0]] == mark and self.board[condition[1]] == mark and self.board[condition[2]] == mark:
                self.gameOver = True

