import os
import time
import datetime
from dotenv import load_dotenv
import discord
from discord import colour
import requests
from discord.ext import commands
from string import printable
import platform
import asyncio

load_dotenv()
OPEN_WEATHER_MAP_KEY = os.getenv('OPEN_WEATHER_MAP_KEY')

def setup(bot):
    bot.add_cog(Miscellaneous(bot))

class Miscellaneous(commands.Cog):

    def __init__(self,bot):
        self.bot = bot



    @commands.command(name="meme")
    async def meme(self,ctx):
        '''Generate Random memes.'''
        r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
        data = r.json()
        e = discord.Embed()
        e.set_image(url=data["url"])
        await ctx.send(embed=e)


    @commands.command(name="def")
    async def urban(self,ctx, word):
        '''Defines any word you type.'''
        data= requests.get(f"http://api.urbandictionary.com/v0/define?term={word}").json()
        top = data['list'][0]
        definition=f"{top['definition'].replace('[','').replace(']','')}"
        e = discord.Embed(title=f"{word.title()}",
                description=definition, color=0x00ff00)
        await ctx.send(embed=e)

    @commands.command(name="advice")
    async def advice(self,ctx):
        '''Generate random lief advice'''
        r = requests.get("https://api.adviceslip.com/advice")
        data = r.json()
        await ctx.send(data["slip"]["advice"])

    @commands.command()
    async def echo(self,ctx, *args):
        ''' Reapeat whatever you type after !echo '''
        await ctx.send(' '.join(args))

    @commands.command()
    @commands.guild_only()
    async def annoy(self,ctx,user: discord.Member = None,num = 10):
        ''' Annoy Whoever you mention, ecept the egg MoMo '''
        if user:
            if user.id == 787194682354040833:
                await ctx.send("No hahahahaahaaaaaaaaa get siked")
            else:
                for _ in range(num):
                    await ctx.send(f"{str(user.mention)}, عم اجرب صوتيييي")

    @commands.command(name = "server")
    @commands.guild_only()
    async def server_info(self,ctx):
        '''Display basic server info'''
        guild = ctx.guild
        embed=discord.Embed(color=0xffffff)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Server name", value=guild.name, inline=False)
        embed.add_field(name="Size", value=guild.member_count, inline=False)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
        await ctx.send(embed=embed)


    @commands.command(name="weather",aliases=["طقس"], )
    async def weather(self,ctx,city,lang ='en'):
        '''Shows the weather of the Country you entered.'''
        if not not bool(set(city) - set(printable)) :
            lang = "ar"
        msg = await ctx.send("Measuring...")    
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_MAP_KEY}&units=metric&lang={lang}"
        data = requests.get(url).json()
        if data['cod'] != 200:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name=f"Error!", value=f"We could not find that city!", inline=False)
            return await msg.edit(content="",embed=embed)   
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
        
        return await msg.edit(content="",embed=embed)


    @commands.command()
    async def ping(self,ctx):
        '''Check the bot's ping'''
        embed=discord.Embed(title="Pong!", color=0x00ff1e)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency,4)}ms", inline=False)
        await ctx.send(embed=embed)


    @commands.command(name = "avatar")
    async def avatar(self, ctx, avamember : discord.Member=None):
        ''' Show the users Avatar '''

        embed = discord.Embed(colour = discord.Colour.orange())
        if not avamember:
            avamember = ctx.author
        embed.set_author(name=f"{avamember}", icon_url=avamember.avatar_url)
        userAvatarUrl = avamember.avatar_url
        embed.set_image(url = f"{userAvatarUrl}")
        embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command()
    # @commands.guild_only()
    async def poll(self,ctx,question,minutes = 1):
        minutes_added = datetime.timedelta(minutes = minutes)
        ends_at = datetime.datetime.now() + minutes_added
        embed=discord.Embed(title=f"{question}", description=f'(ends at {ends_at.strftime("%H:%M")})', color=0xd2ba1e)
        embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        msg = await msg.channel.fetch_message(msg.id)
        t_end = time.time() + 60 * minutes # create a timeout timer for how long user can switch page
        while time.time() < t_end: # while time is still ok
            await asyncio.sleep(1)
        msg = await msg.channel.fetch_message(msg.id)
        reactions = msg.reactions
        yes,no =0,0 
        for reaction in reactions:
            if str(reaction.emoji) == '✅':
                yes = reaction.count
            elif str(reaction.emoji) == '❌':
                no = reaction.count
        if yes == no:
            embed=discord.Embed(color=0x0000ff)
            embed.add_field(name=f"Result for '{question}'", value="it is a tie!", inline=False)
            return await ctx.send(embed=embed)
        elif yes > no:
            embed=discord.Embed(color=0x00ff00)
            embed.add_field(name=f"✅ Result for '{question}'", value="The people voted yes!", inline=False)
            return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name=f"❌ Result for '{question}'", value="The people voted no!", inline=False)
            return await ctx.send(embed=embed)




    @commands.command()
    async def slap(self, ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
        ''' Slap any user you want to punish :3 '''
        slapped = ", ".join(x.name for x in members)
        await ctx.send('{} just got slapped for {}'.format(slapped, reason))
