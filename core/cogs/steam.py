import discord
from core.ext.steamio import Client
from discord.ext import commands, menus
from typing import Optional
from asyncpg import UniqueViolationError
from ..ext.pagination import SimplePages

client = Client(key='B60B0B099B78C82681C16F988FBFE500')

class Steam(commands.Cog, name="<:steam:767575677394223114> Steam"):
    """Commands related to the steam api."""
    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    async def steam(self, ctx):
        pass

    @steam.command()
    async def login(self, ctx, steamid = None):
        '''Stores your steam id in the database.'''
        if not steamid:
            return await ctx.send("You must provide your steam id.")

        try:
            await self.bot.pool.execute("INSERT INTO steam(id, author_id) VALUES($1, $2)", int(steamid), int(ctx.author.id))
            await ctx.send("Ok")
        except UniqueViolationError:
            return await ctx.send("Steam id already in database.")

    @steam.command(name='twab', hidden=True)
    async def twab(self, ctx, gameid = 1085660):
        req = await client.get_news(gameid)
        e = discord.Embed(description=req.title)
        page = SimplePages(entries=[*req.ext.values()], per_page=12)
        try:
            await page.start(ctx)
        except menus.MenuError as e:
            await ctx.send(e)

     
    @steam.command()
    async def bans(self, ctx, user: Optional = None):
        """Shows a user's steam bans."""
        user = await self.bot.pool.fetchrow("SELECT id FROM steam WHERE author_id = $1", ctx.author.id)
        player = await client.get_bans(user['id'])
        sir = await client.get_user(user['id'])
        url = f"https://steamcommunity.com/profiles/{user['id']}"
        e = discord.Embed(color=discord.Color.dark_theme())
        # e.set_image(url=avatar.avatar)
        e.set_author(name=player.id)
        e.add_field(name="Profile", value=f"[{sir.name}]({url})")
        e.add_field(name="VAC Banned?", value=player.vac)
        e.add_field(name="Last Ban", value=player.last_ban)
        e.add_field(name="Number Of Bans", value=player.count)
        e.add_field(name="Communiy Banned?", value=player.community)
        e.add_field(name="Economy Bans", value=player.economy_ban)
        await ctx.send(embed=e)

    @steam.command()
    async def friends(self, ctx, user = None):
        '''Show a user's steam friends.'''
        friend = await client.get_friends(user)
        p = SimplePages(entries=friend.total, per_page=10)
        try:
            await p.start(ctx)
        except menus.MenuError as e:
            await ctx.send(e)


    @steam.command(aliases=['lp'])
    async def lastplayed(self, ctx, user = None):
        if user == 'fate':
            user = 76561198141430157
        elif user == 'karl':
            user = 76561198982884996
        last = await client.get_last_played(user)
        p = SimplePages(entries=last.name, per_page=10)
        try:
            await p.start(ctx)
        except menus.MenuError as e:
            await ctx.send(e)


    @steam.command()
    async def user(self, ctx, user):
        '''Shows info about a steam user.'''
        data = await client.get_user(user)
        e = discord.Embed(description=f"[Profile url]({''.join(data.url)})", color=discord.Color.dark_theme())
        e.set_author(name=data.name)
        e.set_image(url=data.avatar)

        e.add_field(name="Playing now", value=data.playing_now)
        e.add_field(name="Game ID", value=data.game_id)

        e.add_field(name="Country", value=data.country_flag if data.country_flag else None)

        e.add_field(name='Player ID', value="".join(data.id), inline=True)
        e.add_field(name='Clan ID', value="".join(data.clan_id if data.clan_id else 'No clan.'))
        try:
            await ctx.send(embed=e)
        except AttributeError as e:
            await ctx.send(f"```\n{e}\n```")

def setup(bot):
    bot.add_cog(Steam(bot))