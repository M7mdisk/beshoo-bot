import os
from string import printable                                                                                                                                                                           
import discord
import requests
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()  
intents.members = True
bot= Bot(command_prefix = '!',intents=intents)
OPEN_WEATHER_MAP_KEY = "ea073e04bc85f31dab1408ad497f277f"

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