import discord
from discord.ext.commands import command, Cog, group
from data import config
import random
import sr_api as sr
from ..ext.utils import color
from typing import Any, Optional
from ..ext import HTTPClient
from jishaku.paginators import PaginatorInterface, WrappedPaginator

class Fun(Cog, name="\U0001f3d3 Fun"):
    def __init__(self, bot):
        self.bot = bot
        self.session = sr.Client()
        self._http = HTTPClient()



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

    @command(name='animal')
    async def random_cat(self, ctx, animal: str):
        '''Random animal picture.'''
        coro = await self.session.get_image(animal)
        embed = discord.Embed(
            color=color.invis(self)
        )
        embed.set_image(url=coro.url)
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



    @command(name='define', aliases=['def'])
    async def define(self, ctx, *, word: str):
        try:
            coro = await ctx.http.get(
                "https://mashape-community-urban-dictionary.p.rapidapi.com/define", 
                headers = {
                        'x-rapidapi-key': config.rapid_api,
                        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
                        },
                params = {"term": word.lower()}
                )
            real = [i.get('definition') for i in coro.get('list')]
            vots = [i.get('thumbs_up') for i in coro.get('list')]
            votedown = [i.get('thumbs_down') for i in coro.get('list')]
            date = [i.get('written_on') for i in coro.get('list')]
            url = [i.get('permalink') for i in coro.get('list')]
            author = [i.get('author') for i in coro.get('list')]
            e = discord.Embed(title=f"ThumbsUp ```{vots[0]}``` | ThumbsDown ```{votedown[0]}```", description=real[0])
            e.set_author(name=author[0], url=url[0])
            e.set_footer(text=date[0])
            await ctx.send(embed=e)
        except IndexError:
            return await ctx.send("Didn't find anything.")

def setup(bot):
    bot.add_cog(Fun(bot))