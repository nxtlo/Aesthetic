import discord
from discord.ext.commands import command, Cog, group
import random
import aiohttp
import json
from ..ext.utils import color

class Fun(Cog, name="\U0001f3d3 Fun"):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()



    @command(name="joke")
    async def random_joke(self, ctx):
        async with self.session as cs:
            async with cs.get("https://official-joke-api.appspot.com/jokes/random") as r:

                data = await r.json()

                e = discord.Embed(
                    title=data['setup'],
                    description=data['punchline'],
                    color=color.invis(self)
                )
                await ctx.send(embed=e)




    @command(name="pik")
    async def random_pic(self, ctx):
        async with self.session as s:
            async with s.get("https://some-random-api.ml/img/pikachu") as r:

                data = await r.json()

                e = discord.Embed(
                    title="Random picture",
                    color=color.invis(self)
                )
                e.set_image(url=data['link'])
                e.set_footer(text=ctx.author.name)
                await ctx.send(embed=e)
                



    @command(name="quote")
    async def rancom_joke(self, ctx):
    
        with open("./data/choises.txt", "r") as r:
            reads = r.readlines()

        nil = random.choice(reads)
        
        await ctx.send(nil)

    @command(name='cat')
    async def random_cat(self, ctx):
        async with self.session as cs:
            async with cs.get("http://aws.random.cat/meow") as r:
                
                data = await r.json()
                img = 'https://kittenrescue.org/wp-content/uploads/2016/11/KittenRescue-TheKRCatSanctuary.png'
                
                embed = discord.Embed(
                    title="Kitten",
                    color = ctx.author.color
                )
                embed.set_image(url=data['file'])
                embed.set_footer(text='random cat', icon_url=img)
                await ctx.send(embed=embed)



    @command(name='dog')
    async def random_dog(self, ctx):
        async with self.session as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                
                data = await r.json()
                embed = discord.Embed(
                    title="Doggo",
                    color = ctx.author.color
                )
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)


    @command(name='fox')
    async def random_fox(self, ctx):
        async with self.session as cs:
            async with cs.get("https://some-random-api.ml/img/fox") as r:
                data = await r.json()

                embed = discord.Embed(
                    title='Fox',
                    color = ctx.author.color
                )
                embed.set_image(url=data['link'])
                await ctx.send(embed=embed)

    @command(name='meme')
    async def random_meme(self, ctx):
        async with self.session as cs:
            async with cs.get("https://some-random-api.ml/meme") as r:
                data = await r.json()

                embed = discord.Embed(
                    title='random meme',
                    color = ctx.author.color
                )
                embed.set_image(url=data['image'])
                await ctx.send(embed=embed)

        
def setup(bot):
    bot.add_cog(Fun(bot))