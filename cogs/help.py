from os import name
import discord
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
import time

from requests import __title__


class HELP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="help")
    async def pages(self,ctx):
        author = ctx.message.author
        user = discord.User.id
        embed1 = discord.Embed(color = discord.Colour.orange())
        embed1.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        embed1.title = "A list of all بشير's commands"
        embed1.description = "Miscellaneous:"
        embed1.add_field(name='!meme', value='Generate Random memes.', inline=False)
        embed1.add_field(name='!def < Word >', value='Defines any word you type.', inline=False)
        embed1.add_field(name='!advice', value='Generate Random life advice.', inline=False)
        embed1.add_field(name='!weather < Country >', value='Shows the weather of the Country you entered.', inline=False)
        embed1.set_footer(text="page 1/6")
        # ===================================
        embed2 = discord.Embed(color = discord.Colour.orange())
        embed2.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        embed2.title = "A list of all بشير's commands"
        embed2.description = "Admin:"
        embed2.add_field(name='!kick < @user >', value='Kicks selected member.', inline=False)
        embed2.add_field(name='!ban < @user >', value='Ban selected member.', inline=False)
        embed2.add_field(name='!mute < @user >', value='Mute selected member.', inline=False)
        embed2.set_footer(text="page 2/6")
        # ====================================
        embed3 = discord.Embed(color = discord.Colour.orange())
        embed3.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        embed3.title = "A list of all بشير's commands"
        embed3.description = "Tic Tac Toe:"
        embed3.add_field(name='!tictactoe < @user > < @user >', value='Starts a new game.', inline=False)
        embed3.add_field(name='!endgame', value='Abort the game.', inline=False)
        embed3.add_field(name='!place < field number >', value='place a mark on selected field number.', inline=False)
        embed3.set_footer(text="page 3/6")
        # =====================================
        embed4 = discord.Embed(color = discord.Colour.orange())
        embed4.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        embed4.title = "A list of all بشير's commands"
        embed4.description = "Voice Channel:"
        embed4.add_field(name='!join', value='Join\'s a voice channel.', inline=False)
        embed4.add_field(name='!play < youtube URL >', value='Downloads the music then start playing it.', inline=False)
        embed4.add_field(name='!leave < field number >', value='Leaves the voice channel.', inline=False)
        embed4.set_footer(text="page 4/6")
        # ======================================


        embeds = [embed1, embed2, embed3, embed4] # your  embeds here
        i=0

        # send the first embed and add reactions
        msg = await ctx.send(embed=embeds[0])
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

        # check statment for when reaction is added
        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '◀️' or str(reaction.emoji) == '▶️' )


        t_end = time.time() + 60 * 2 # create a timeout timer for how long user can switch pages (2 minutes)
        while time.time() < t_end: # while time is still ok
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check) # wait for the reaction from a user
            if str(reaction.emoji) == '◀️':
                await msg.remove_reaction("◀️", user)
                if user == ctx.author and i >0:
                    i-=1 # change the index accordingly
                    await msg.edit(embed = embeds[i]) # edit the message
            elif str(reaction.emoji) == '▶️':
                await msg.remove_reaction("▶️", user)
                if user == ctx.author and i <len(embeds)-1:
                    i+=1 # change the index accordingly
                    await msg.edit(embed = embeds[i]) # edit the message