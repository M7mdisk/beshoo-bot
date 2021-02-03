import discord
from discord import embeds
from discord.ext import commands
from os import name
from discord.ext.commands import cog
import aiohttp
import requests
from imgurpython import ImgurClient

class random(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data = None
        self.embed = None


    @commands.command(name = "cat")
    async def random_cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://aws.random.cat/meow") as r:
                self.data = await r.json()
                self.embed = discord.Embed(title="Meow")
                self.embed.set_image(url=self.data["file"])
                self.embed.set_footer(text="http://random.cat/meow")

                await ctx.send(embed=self.embed)


    @commands.command(name = "dog")
    async def random_dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                self.data = await r.json()
                self.embed = discord.Embed(title="Woof")
                self.embed.set_image(url=self.data["url"])
                self.embed.set_footer(text="https://random.dog/")

                await ctx.send(embed=self.embed)
        
