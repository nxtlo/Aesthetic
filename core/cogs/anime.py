from discord.ext.commands import command, group, Cog
from discord import Embed
from ..ext.utils import color
import requests
from mal import AnimeSearch, Anime, MangaSearch
from typing import Union, Any, Optional

class _Anime(Cog, name="\U0001f48c Anime"):
    '''Commands to give you info about a manga/anime.'''
    def __init__(self, bot):
        self.bot = bot
        self.anime = AnimeSearch
        self.clean_anime = Anime
        self.manga = MangaSearch


    @command(name="anime", aliases=['ani'])
    async def _anime(self, ctx, *, anime: str):
        """Get info about your favorite anime"""

        rest = self.anime(anime)
        anime_ = rest.results[0]
        img = anime_.image_url
        title = anime_.title
        eps = anime_.episodes
        url = anime_.url
        info = anime_.synopsis
        genere = anime_.type
        score = anime_.score
        hyperlink = f"[{title}]({url})"

        e = Embed(description=info)
        e.add_field(name="Anime Link", value=hyperlink)
        e.color = color.random(self)
        e.set_image(url=img)
        e.add_field(name='Type', value=genere)
        e.add_field(name='Episodes', value=eps)
        e.add_field(name="Rating", value=score)
        await ctx.send(embed=e)

    @command(name="manga", aliases=['mang', 'man'])
    async def _mnga(self, ctx, *, manga: str):
        
        rest = self.manga(manga).results[0]
        img = rest.image_url
        score = rest.score
        genere = rest.type
        info = rest.synopsis
        url = rest.url
        title = rest.title
        eps = rest.volumes
        hyperlink = f"[{title}]({url})"

        e = Embed(description=info)
        e.add_field(name="Manga Link", value=hyperlink)
        e.color = color.random(self)
        e.set_image(url=img)
        e.add_field(name='Genere', value=genere.format('utf-8'))
        e.add_field(name='Chapters', value=eps)
        e.add_field(name="Rating", value=score)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(_Anime(bot))