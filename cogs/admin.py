import discord
from discord.ext import commands
from discord import Permissions
import asyncio

def setup(bot):
    bot.add_cog(Administration(bot))

class Administration(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def kick(self,ctx, member: discord.Member, *, why=None):
        ''' Kick a member from the server '''
        await member.kick(reason=why)
        await ctx.channel.send(f"**{member} has been kicked from this server by {ctx.author}**")


    @kick.error
    async def kick_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("Looks like you don't have the perm.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self,ctx, member: discord.Member):
        ''' Mute the member '''
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if role not in guild.roles:
            perms = discord.Permissions(send_messages=False, speak=False)
            await guild.create_role(name="Muted", permissions=perms)
            await member.add_roles(role)
            await ctx.send(f"{member} was muted.")
        else:
            await member.add_roles(role) 
            await ctx.send(f"{member} was muted.")     

    @mute.error
    async def mute_error(self,ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You are not an admin") 
        elif isinstance(error, commands.BadArgument):
            await ctx.send("That is not a valid member") 

    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban (self,ctx, member:discord.User=None, reason =None):
        ''' Ban a member from the server '''
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot ban yourself")
            return
        if reason == None:
            reason = "For being a jerk!"
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member.mention} is banned! :hammer: :hammer: :hammer:")
        await member.send(message)

    @ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the premissions to do that") 
        elif isinstance(error, commands.BadArgument):
            await ctx.send("That is not a valid member") 





    @commands.command(name = "clear")
    async def clear(self, ctx, amount=10):
        ''' Clear chat messages (Admins Only) '''
        await ctx.channel.purge(limit=amount)
        msg = await ctx.channel.send(f"{amount} messages deleted!")
        await asyncio.sleep(2)
        await msg.delete()



    @commands.command(name="dm")
    async def send_dm(self, ctx, member: discord.Member, content):
        ''' Sends a message to a user in his DMs '''
        channel = await member.create_dm()
        await channel.send(content)