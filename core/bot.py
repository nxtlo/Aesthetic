from pathlib import Path
from discord import Intents, Message, Member, __version__
from discord.ext.commands import when_mentioned_or, Bot
from discord.ext import commands
from time import sleep
from core.cogs.commands import FetchedUser
from data import config
from core.ext.utils import color

import datetime
import asyncio
import discord
import os
import copy
import logging
import traceback
import sys
from aiopyql.data import Database as db


COGS = (
    'jishaku',
    'core.cogs.c',
    'core.cogs.tools',
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
        # self._cogs = [p.stem for p in Path(".").glob("./core/cogs/*.py")]
        self._owner = 350750086357057537

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

    # next funcs just to make me run queries easier

    async def fetch(self, *, table):
        try:
            return await self.pool.tables[table].select('*')
        except Exception:
            raise


    async def query(self, query: str) -> None:
        try:
            return await self.pool.run(query)
        except Exception:
            raise

    async def on_ready(self):
        self.uptime = datetime.datetime.utcnow()
        print("Bot ready.")
        print('Logged in as:\n')
        print('Bot name:\n', self.user.name)
        print('Bot id:\n',self.user.id)
        print('Discord Version:\n', __version__)

        # Create and prepare the prefix table. 
        try:
            if not 'prefixes' in self.pool.tables:
                await self.pool.create_table(
                    'prefixes',
                    [
                        ('id', str),
                        ('prefix', str)
                    ],
                    prim_key='id'
                )
            else:
                return
        except Exception:
            raise

    # idk why i did this but yeh :<|
    async def get_prefix(self, message):
        pfx = await self.pool.tables['prefixes'].select(
            'prefix',
            where={
                'id': message.guild.id
            }
        )
        if message.guild is None:
            return ('a.', 'a!')
        if not pfx:
            return when_mentioned_or("a.", "a!")(self, message)
        return when_mentioned_or(pfx[0]['prefix'])(self, message)

    async def pool_connect(self) -> db.create:
        self.pool: db.create() = await db.create(
            database=config.database,
            user=config.db_user,
            password=config.password,
            host=config.host,
            port=config.port,
            db_type=config.db_type,
            cache_enabled=True, # Enable db read caching
            max_cache_len=256)

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)
        ctx = await self.get_context(message)
        if ctx.invoked_with and ctx.invoked_with.lower() not in self.commands and ctx.command is None:
            msg = copy.copy(message)
            if ctx.prefix:
                new_content = msg.content[len(ctx.prefix):]
                msg.content = "{}tag get {}".format(ctx.prefix, new_content)
                await self.process_commands(msg)
                

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
