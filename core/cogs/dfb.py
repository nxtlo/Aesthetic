import httpx
import asyncio
import discord
from discord.ext import commands
from typing import Optional, Dict


class BfDClient:
    """
    smol async wrapper for botsfordiscord.com api.
    """
    __slots__ = ('session', 'token')
    BASE = 'https://botsfordiscord.com/api/'

    def __init__(self, session: httpx.AsyncClient = None, token: str = None):
        self.session = session
        self.token = token


    def __repr__(self):
        return f"Session: {self.session}, Class: {self.__class__}"


    async def init_session(self) -> Optional[httpx.AsyncClient]:
        self.session = httpx.AsyncClient()


    async def close(self):
        if not self.session.is_closed:
            try:
                await self.session.aclose()
            except httpx.CloseError as exc:
                raise f"Error closing the session due to {exc.with_traceback()}"

    async def fetch(self, path):
        if not self.session:
            await self.init_session()

        async with self.session as client:
            data = await client.get(self.BASE + path)
            try:
                if data.status_code == 200:
                    return data.json()
            except httpx.RequestError as exc:
                raise exc

    async def fetch_user(self, userid: int) -> None:
        return await self.fetch(f'user/{userid}')


    async def fetch_bot(self, botid: int) -> None:
        return await self.fetch(f'bot/{botid}')


    async def fetch_user_bots(self, user: int) -> None:
        return await self.fetch(f"user/{user}/bots")


class BotsForDiscord(commands.Cog, name="<:botsfordiscord2:381674698993303553> BotsForDiscord"):
    """Commands related to BotsForDiscord API"""
    def __init__(self, bot):
        self.bot = bot
        self._client = BfDClient()

    
    @commands.group()
    async def bfd(self, ctx):
        """bfd's subcommands"""
        pass

    @bfd.command(name='whoadd')
    async def _bfd_bot(self, ctx, botid = None):
        """Gives you information about a bot in BfD"""
        if not botid:
            return await ctx.send("Bot's id most be provided.")

        boto = await self._client.fetch_bot(botid)

        try:

            e = discord.Embed(title=boto['tag'], description=boto['short_desc'])
            e.set_author(name=f"")

            e.add_field(name='Owner', value=f"<@{boto['owner']}>")
            e.add_field(name='Status', value=boto['status'])
            e.add_field(name='Votes', value=boto['votes'])
            
            if boto['support_server']:
                e.add_field(name='Support Server', value=f"[JumpTo]({boto['support_server']})")

            if boto['owners']:
                e.add_field(name='Owners', value=boto['owners'])

            if boto['github']:
                e.add_field(name='Github Repo', value=f"[JumpTo]({boto['github']})")

            e.add_field(name='Guild count', value=boto['server_count'])
            e.add_field(name='Bot Library', value=boto['library'])
            e.add_field(name='Verified?', value=boto['verified'])
            e.add_field(name='Approved?', value=boto['approved'])
            e.add_field(name='Featured?', value=boto['featured'])
            e.add_field(name='Partnered?', value=boto['partner'])
            e.add_field(name='Prefixes', value=boto['prefix'])
            e.set_footer(text=f"Tags: {boto['tags']}")
            await ctx.send(embed=e)
        except TypeError:
            await ctx.send(f"Bot {botid} not found.")
        

    @bfd.command(name='whois')
    async def dfb_user(self, ctx, user: int = None):
        """Gives you information about a user in BfD"""
        user = user or ctx.author.id
        query = await self._client.fetch_user(user)

        try:
            e = discord.Embed(title=query['username'], description=query['bio'])
            e.add_field(name='Status', value=query['status'])
            e.add_field(name='Discord User', value=f"<@{query['id']}>")
            e.add_field(name='Is Admin?', value=query['isAdmin'])
            e.add_field(name='Covid Funder?', value=query['covidFund'])
            e.add_field(name='Is Mod?', value=query['isMod'])
            e.add_field(name='Is JrMod?', value=query['isJrMod'])
            e.add_field(name='Is Beta?', value=query['isBeta'])
            e.add_field(name='Is Partner?', value=query['isPartner'])
            if query['website']:
                e.add_field(name='Website', value=f"[Website]({query['website']})")
            await ctx.send(embed=e)
        except TypeError:
            await ctx.send(f"Member {user} Not found.")


    @bfd.command(name='hasbots')
    async def _has_bots(self, ctx, user: int = None):
        """Shows the user-bots."""
        user = user or ctx.author.id
        query = await self._client.fetch_user_bots(user)

        def fmt() -> discord.Embed:
            e = discord.Embed()
            return e.add_field(name="Found bots", value=f'\n'.join(f"<@{q}>" for q in [*query['bots']]))

        try:
            await ctx.send(embed=fmt())
        except TypeError:
            await ctx.send(f"Member {user} has No bots.")

def setup(bot):
    bot.add_cog(BotsForDiscord(bot))