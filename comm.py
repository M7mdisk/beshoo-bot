import requests
import discord

async def meme(ctx):
    r = requests.get("https://meme-api.herokuapp.com/gimme/memes")
    data = r.json()
    e = discord.Embed()
    e.set_image(url=data["url"])
    return ctx.send(embed=e)


async def advice(ctx):
    r = requests.get("https://api.adviceslip.com/advice")
    data = r.json()
    return ctx.send(data["slip"]["advice"])