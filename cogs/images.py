import discord
import requests
from discord.ext import commands
from PIL import Image
from io import BytesIO
import time


IMAGGA_KEY = 'acc_21a00bb908a921c'
IMMAGA_SECRET = 'd53d2e2aa574137d106da75aca37c743'

class Images(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def face(self,ctx,):
        url= "https://api.imagga.com/v2/faces/detections?return_face_attributes=1&image_url="
        
        if not ctx.message.attachments :
            return await ctx.send("Attach an image!")
        url+=ctx.message.attachments[0].url

        # Send request to API 
        r = requests.get(url,auth=(IMAGGA_KEY,IMMAGA_SECRET))
        data = r.json()
        # Check for errors
        if data["status"]["type"] !=  "success":
            embed=discord.Embed(title="Something went Wrong!", color=0xff0000)
            embed.add_field(name="Error", value=data["status"]["text"], inline=False)
            return await ctx.send(embed=embed)

        # Load image to be cropped as thumbnail
        if not data["result"]["faces"]:
            embed=discord.Embed(title="No faces found", color=0xff0000)
            return await ctx.send(embed=embed)
        embeds = []
        n=len(data["result"]["faces"])
        # Generate embeds with data displayed
        for i,face in  enumerate(data["result"]["faces"]):
            embed=discord.Embed(color=0x00ff00)
            coords=face["coordinates"]
            thumb = f"https://crop-api.herokuapp.com/crop/?url={ctx.message.attachments[0].url}&xmin={coords['xmin']}&ymin={coords['ymin']}&xmax={coords['xmax']}&ymax={coords['ymax']}"
            embed.set_thumbnail(url=thumb)
            embed.add_field(name=f"Face #{i+1}/{n}", value=f"{round(face['confidence'],1)}% confident", inline=False)
            for attribute in face["attributes"]:
                embed.add_field(name=f"{attribute['type'].title()}", value=f"{attribute['label'].title()} ({round(attribute['confidence'],1)}%)", inline=False)
            embeds.append(embed)

        if len(embeds) == 1:
            return  await ctx.send(embed=embeds[0])
        i = 0

        msg = await ctx.send(embed=embeds[0])
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")        
        def check(reaction, user):
            return user != self.bot.user and (str(reaction.emoji) == '◀️' or str(reaction.emoji) == '▶️' )
        t_end = time.time() + 60 * 10
        while time.time() < t_end:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '◀️':
                await msg.remove_reaction("◀️", user)
                if user == ctx.author and i >0:
                    i-=1
                    await msg.edit(embed = embeds[i])
            elif str(reaction.emoji) == '▶️':
                await msg.remove_reaction("▶️", user)
                if user == ctx.author and i <len(embeds)-1:
                    i+=1
                    await msg.edit(embed = embeds[i])


    # Command below can be utalized for editing images without files.

    # @commands.command()
    # async def pages(self,ctx,n=3):
    #     i = 1
    #     embed=discord.Embed(color=0x00ff00)
    #     embed.add_field(name=f"Page {i}", value=f"asdf", inline=False)
    #     msg = await ctx.send(embed=embed)
    #     await msg.add_reaction("◀️")
    #     await msg.add_reaction("▶️")
    #     def check(reaction, user):
    #         return user == ctx.author and (str(reaction.emoji) == '◀️' or str(reaction.emoji) == '▶️' )
    #     t_end = time.time() + 60 * 2
    #     while time.time() < t_end:
    #         reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
    #         if str(reaction.emoji) == '◀️':
    #             await msg.remove_reaction("◀️", user)
    #             i-=1
    #         elif str(reaction.emoji) == '▶️':
    #             await msg.remove_reaction("▶️", user)
    #             i+=1
    #         embed=discord.Embed(color=0x00ff00)
    #         embed.add_field(name=f"Page {i}", value=f"asdf", inline=False)
    #         print("reacted?")
            
    #         await msg.edit(content="",embed=embed)


    @commands.command()
    async def bgremove(self,ctx):
        '''Remove Background from image!
        '''
        url = "https://background-removal.p.rapidapi.com/remove"
        # pic_ext = ['.jpg','.png','.jpeg']
        if not ctx.message.attachments :
            return await ctx.send("Attach an image!")
        payload = f"image_url={ctx.message.attachments[0].url}"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'x-rapidapi-key': "157b8ea155msh5a9d9520fc875b8p1d5754jsn1f29da0cc7a7",
            'x-rapidapi-host': "background-removal.p.rapidapi.com"
            }
        msg = await ctx.send("Working on it...")
        r = requests.request("POST", url, data=payload,headers=headers)
        data = r.json()
        embed=discord.Embed(title="Done!", url=data["response"]["image_url"])
        embed.set_image(url=data["response"]["image_url"])
        embed.set_footer(text=f"Time: {r.elapsed.total_seconds()}")
        await msg.edit(content="",embed=embed)
