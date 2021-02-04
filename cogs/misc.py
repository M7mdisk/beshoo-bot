import discord
import requests
from discord.ext import commands
from string import printable                                                                                                                                                                           
import os
import platform
OPEN_WEATHER_MAP_KEY = "ea073e04bc85f31dab1408ad497f277f"
class Miscellaneous(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="meme")
    async def meme(self,ctx):
        r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
        data = r.json()
        e = discord.Embed()
        e.set_image(url=data["url"])
        await ctx.send(embed=e)


    @commands.command(name="def")
    async def urban(self,ctx, word):
        data= requests.get(f"http://api.urbandictionary.com/v0/define?term={word}").json()
        top = data['list'][0]
        definition=f"{top['definition'].replace('[','').replace(']','')}"
        e = discord.Embed(title=f"{word.title()}",
                description=definition, color=0x00ff00)
        await ctx.send(embed=e)

    @commands.command(name="advice")
    async def advice(self,ctx):
        r = requests.get("https://api.adviceslip.com/advice")
        data = r.json()
        await (data["slip"]["advice"])

    @commands.command()
    async def echo(self,ctx, *args):
        await ctx.send(' '.join(args))

    @commands.command()
    @commands.guild_only()
    async def annoy(self,ctx,user: discord.Member = None,num = 10):
        if user:
            if user.id == 787194682354040833:
                await ctx.send("No hahahahaahaaaaaaaaa get siked")
            else:
                for _ in range(num):
                    await ctx.send(f"{str(user.mention)}, عم اجرب صوتيييي")

    @commands.command(name = "server")
    @commands.guild_only()
    async def server_info(self,ctx):
        guild = ctx.guild
        embed=discord.Embed(color=0xffffff)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Server name", value=guild.name, inline=False)
        embed.add_field(name="Size", value=guild.member_count, inline=False)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
        await ctx.send(embed=embed)


    @commands.command(name="weather",aliases=["طقس"], )
    async def weather(self,ctx,city,lang ='en'):
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
        if platform.system() == "Linux":
            stream = os.popen(r"vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
            temp = stream.read()
        embed=discord.Embed(title="Pong!", color=0x00ff1e)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency,1)}ms", inline=False)
        if platform.system() == "Linux":
            embed.add_field(name="Temperature", value=f"{temp[:-1]}°c", inline=True)
        await ctx.send(embed=embed)
    
