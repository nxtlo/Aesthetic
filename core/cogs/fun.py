import discord
from discord.ext.commands import command, Cog, group
import random
import aiohttp
import json
import sr_api as sr
from ..ext.utils import color
from animals import Animals
from typing import Any, Optional
from sr_api.image import Image
from jishaku.paginators import PaginatorInterface, WrappedPaginator

class Fun(Cog, name="\U0001f3d3 Fun"):
    def __init__(self, bot):
        self.bot = bot
        self.animal = Animals
        self.session = sr.Client()



    @command(name='techf')
    async def tech_fact(self, ctx):
        '''gives a random fact about Tech'''
        try:
            with open('data/facts.txt', 'r', encoding='utf-8') as r:
                facts = r.readlines()
                r_fact = random.choice(facts)
                await ctx.send(r_fact)
        except Exception as e:
            pass



    @command(name="joke")
    async def random_joke(self, ctx):
        '''Random joke.'''
        e = discord.Embed(
            description = await self.session.get_joke(),
            color=color.invis(self)
        )
        await ctx.send(embed=e)


    @command(name="pik")
    async def random_pic(self, ctx):
        '''Random pikachu picture.'''
        pika = await self.session.get_image(name='pikachu')
        e = discord.Embed(
            title="Random Pikachu",
            color=color.invis(self)
        )
        e.set_image(url=pika)
        e.set_footer(text=ctx.author.name)
        await ctx.send(embed=e)


    @command(name="quote")
    async def rancom_joke(self, ctx):
        '''Random quote.'''
        with open("./data/choises.txt", "r") as r:
            reads = r.readlines()

        nil = random.choice(reads)
        
        await ctx.send(nil)

    @command(name='cat')
    async def random_cat(self, ctx):
        '''Random cat picture.'''
        embed = discord.Embed(
            title="Kitten",
            color=color.invis(self)
        )
        embed.set_image(url=self.animal('cat').image())
        await ctx.send(embed=embed)


    @command(name='panda')
    async def random_panda(self, ctx):
        '''Random panda picture'''
        embed = discord.Embed(
            title="Panda",
            color=color.invis(self)
        )
        embed.set_image(url=self.animal('panda').image())
        await ctx.send(embed=embed)


    @command(name='dog')
    async def random_dog(self, ctx):
            '''Random doggo picture :D'''
            embed = discord.Embed(
                title="Doggo",
                color = color.invis(self)
            )
            embed.set_image(url=self.animal('dog').image())
            await ctx.send(embed=embed)


    @command(name='fox')
    async def random_fox(self, ctx):
            '''Random fox picture'''
            embed = discord.Embed(
                title="foxie",
                color = color.invis(self)
            )
            embed.set_image(url=self.animal('fox').image())
            await ctx.send(embed=embed)

    @command(name='meme')
    async def random_meme(self, ctx):
        '''Random meme.'''
        _meme = await self.session.get_meme()
        embed = discord.Embed(
            title=_meme.caption,
            color = color.invis(self)
        )
        embed.set_image(url=_meme.image)
        await ctx.send(embed=embed)


    @command(name='lyric', aliases=['lyrics', 'lyr'])
    async def _lyric(self, ctx, *, song: str = None):
        '''Get the lyrics for a song.'''
        if not song:
            return await ctx.send('No song was provided.')
        else:
            try:
                query = await self.session.get_lyrics(title=song)
                if len(query.lyrics) < 2048:
                    e = discord.Embed(
                                    title=f"Lyrics for {query.title}", 
                                    description=query.lyrics,
                                    color=color.invis(self),
                                    timestamp=ctx.message.created_at)
                    e.set_thumbnail(url=query.thumbnail)
                    await ctx.send(embed=e)
                else:
                    wrapp = WrappedPaginator(prefix='```', suffix='```', max_size=1400)
                    wrapp.add_line(query.lyrics)
                    page = PaginatorInterface(ctx.bot, wrapp, owner=ctx.author)
                    embed = discord.Embed(description=page)
                    await page.send_to(ctx)
                    # await ctx.send(f"Lyrics for the song {query.title} is too long... here's the link {query.link}")
            except Exception as e:
                await ctx.send(e)


    '''@command(name='define', aliases=['def'])
    async def _def(self, ctx, *, name):
        defe = await self.session.define(name)
        try:
            _e = discord.Embed(title = f"{defe.word}'s Definition", color = color.invis(self))
            await ctx.send(embed=_e)
        except Exception as e:
            await ctx.send(e)'''

def setup(bot):
    bot.add_cog(Fun(bot))