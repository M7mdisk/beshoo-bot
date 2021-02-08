from os import name
import discord
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
import time

from requests import __title__

def setup(bot):
    bot.add_cog(Help(bot))

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_guild(self,ctx, command :  str = None):
        '''Displays the help message. ¯\_(ツ)_/¯'''
        if command:
            embed = discord.Embed(color = discord.Colour.red())
            cmd = [x for x in self.bot.commands if x.name.lower() == command.lower()]
            if not cmd:
                embed.add_field(name="Error!", value="No such command", inline=False)
                return await ctx.send(embed=embed)
            else:
                c = cmd[0]
                parent = c.full_parent_name
                if len(c.aliases) > 0:
                    aliases = '|'.join(c.aliases)
                    fmt = f'[{c.name}|{aliases}]' 
                    if parent:
                        fmt = parent + ' ' + fmt
                    alias = fmt
                else:
                    alias = c.name if not parent else parent + ' ' + c.name
                name = f"{self.bot.command_prefix}{alias} {c.signature}"
                embed.add_field(name=name, value=c.help, inline=False)
                return await ctx.send(embed=embed)
        ''' Displays this message. '''
        excluded = ["Administration"]
        cogs_dict = self.bot.cogs
        if isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(title="Help", color = discord.Colour.orange())
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            for cogname,cog in cogs_dict.items():
                commands = cog.get_commands()
                # embed.add_field(name=cogname, value="\u200c", inline=False)
                v = ""
                for c in commands:
                    v+=f"`{c.name}`,"
                embed.add_field(name=cogname, value=v[:-1], inline=True)
            return await ctx.send(embed=embed)

        
        embeds = []
        for cogname,cog in cogs_dict.items():
            if cogname in excluded:
                continue
            embed = discord.Embed(title=cogname, color = discord.Colour.orange())
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            commands = cog.get_commands()
            for c in commands:
                parent = c.full_parent_name
                if len(c.aliases) > 0:
                    aliases = '|'.join(c.aliases)
                    fmt = f'[{c.name}|{aliases}]' 
                    if parent:
                        fmt = parent + ' ' + fmt
                    alias = fmt
                else:
                    alias = c.name if not parent else parent + ' ' + c.name
                name = f"{self.bot.command_prefix}{alias} {c.signature}"
                desc = c.help if c.help else "\u200c"
                embed.add_field(name=name, value=desc, inline=False)
            embeds.append(embed)

        i=0
        # send the first embed and add reactions
        msg = await ctx.send(embed=embeds[0].set_footer(text=f"page {i+1}/{len(embeds)}"))

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
                    await msg.edit(embed = embeds[i].set_footer(text=f"page {i+1}/{len(embeds)}")) # edit the message
            elif str(reaction.emoji) == '▶️':
                await msg.remove_reaction("▶️", user)
                if user == ctx.author and i <len(embeds)-1:
                    i+=1 # change the index accordingly
                    await msg.edit(embed = embeds[i].set_footer(text=f"page {i+1}/{len(embeds)}")) # edit the message

