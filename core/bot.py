from pathlib import Path
from discord import Intents, Message, Member, __version__
from discord.ext.commands import when_mentioned_or, Bot
from discord.ext import commands
from time import sleep
from core.cogs.commands import FetchedUser
from data import config
from core.ext.utils import color
from core.ext.ctx import Context
from typing import Optional, Any, Union, Dict, Tuple

import asyncpg
import datetime
import asyncio
import discord
import os
import copy
import logging
import traceback
import sys
import aiohttp

COGS = (
    'jishaku',
    'core.cogs.tech',
    'core.cogs.profiles',
    #'core.cogs.logging', # still broken
    'core.cogs.anime',
    'core.cogs.nsfw',
    'core.cogs.db',
    'core.cogs.commands',
    'core.cogs.fun',
    'core.cogs.math',
    'core.cogs.mod',
    'core.cogs.owner',
    'core.cogs.tags',
    'core.cogs.tasks'
)

class Amaya(Bot):
    """
    Main `class` for the bot to acually run.
    """
    def __init__(self):
        self._owner = 350750086357057537
        self._log_channel = 789614938247266305
        self.seesion = aiohttp.ClientSession()

        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            intents=Intents.all(),
            owner_id=self._owner)
    

    def _uptime(self):
        now = datetime.datetime.utcnow()
        delta = now - self.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days:
            fmt = '{d} days\n{h} hours\n{m} minutes\nand {s} seconds'
        else:
            fmt = '{h} hours\n{m} minutes\nand {s} seconds'
        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @property
    def fate(self) -> int:
        return self._owner or self.owner_id

    
    async def close(self):
        await self.seesion.close()

    @property
    def amaya(self):
        return self.amaya_channel or None


    @property
    def query(self):
        return self._do_query

    async def script_exe(self, path):
        '''execute `.sql` files.'''
        try:
            with open(path, 'r', encoding='utf-8') as sc:
                return await self.pool.execute(sc.read())
        except Exception:
            raise


    async def _do_query(self, query: str):
        try:
            return await self.pool.fetch(query)
        except Exception as e:
            c = self.get_channel(self._log_channel)
            c.send(f"```\n{e}\n```")


    async def amaya_channel(self, gid: int):
        try:
            query = '''
                    SELECT channel_id
                    FROM amaya
                    WHERE guild_id = $1
                    '''
            await self.pool.fetchval(query, gid)
        except Exception:
            raise

    async def on_ready(self):
        self.uptime = datetime.datetime.utcnow()
        print(f"Bot ready. -> {self.user.id}, {self.user.name}")

    async def get_prefix(self, msg):
        if not msg.guild:
            return ('a.', 'a!')
        else:
            query = 'SELECT prefix FROM prefixes WHERE id = $1'
            prefix = await self.pool.fetchval(query, msg.guild.id)

            if not prefix:
                return commands.when_mentioned_or('a!', 'a.')(self, msg)
            return commands.when_mentioned_or(prefix)(self, msg)

    async def pool_connect(self) -> Optional[asyncpg.pool.Pool]:
        self.pool: asyncpg.create_pool() = await asyncpg.create_pool(
            database=config.database,
            user=config.db_user,
            password=config.password,
            host=config.host,
            port=config.port,
            max_inactive_connection_lifetime=0
        )


    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=Context)

    async def process_commands(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)

        try:
            if ctx.command is None:
                return
            await self.invoke(ctx)
        finally:
            pass

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)
               

    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')

        elif isinstance(err, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="I don't have permissions to do that.",
                colour = color.invis(self)
            )
            await ctx.send(embed=embed)
        
        elif isinstance(err, commands.CommandInvokeError):
            original = err.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)

        elif isinstance(err, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="This command is on cooldown.",
                colour = color.invis(self)
            )
            await ctx.send(embed=embed)


    async def on_guild_join(self, guild: discord.Guild):
        roles = [role.mention for role in guild.roles]
        e = discord.Embed(
            title="Joined a new server!",
            color=color.invis(self),
            timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="Server name", value=guild.name)
        e.add_field(name='Server ID', value=guild.id)
        e.add_field(name="Server Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        e.add_field(name="Server region", value=guild.region)
        e.add_field(name="Boosters", value=guild.premium_subscription_count)
        e.add_field(name="Boost Level", value=guild.premium_tier)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 20 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.get_channel(self._log_channel)
        await chan.send(embed=e)
        print(f"Bot joined {guild.name} at {datetime.utcnow()}")

    async def on_guild_remove(self, guild):
        roles = [role.mention for role in guild.roles]
        e = discord.Embed(
            title="Left a server!",
            color=color.invis(self),
            timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="Server name", value=guild.name)
        e.add_field(name='Server ID', value=guild.id)
        e.add_field(name="Server Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        e.add_field(name="Server region", value=guild.region)
        e.add_field(name="Boosters", value=guild.premium_subscription_count)
        e.add_field(name="Boost Level", value=guild.premium_tier)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 20 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.get_channel(self._log_channel)
        await chan.send(embed=e)
        print(f"Bot left {guild.name} at {datetime.utcnow()}")

    def setup(self):
        print("Loading cogs...")
        for cog in COGS:
            try:
	            self.load_extension(f"{cog}")
	            print(f" Loaded {cog} cog.")
            except Exception:
                print(f'\nFailed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

    def run(self):
        self.setup()
        print("Running bot...")
        super().run(config.bot_token, reconnect=True)