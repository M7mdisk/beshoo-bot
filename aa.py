import requests
import discord
async def advice():
    r = requests.get("https://api.adviceslip.com/advice")
    data = r.json()
    return  data["slip"]["advice"]

async def meme():
    r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
    data = r.json()
    e = discord.Embed()
    e.set_image(url=data["url"])
    return e
