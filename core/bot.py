from discord import Intents, Message, Member, User
from discord.ext.commands import when_mentioned_or, Bot
from discord.ext import commands
from data import config
from core.ext.utils import color
from core.ext.ctx import Context
from typing import Optional

import datetime
import time
import discord
import traceback
import sys

COGS = (
    'jishaku',
    # 'core.cogs.steam',
    # 'core.cogs.destiny',
    'core.cogs.ccode',
    'core.cogs.dfb',
    'core.cogs.nuance',
    'core.cogs.profiles',
    #'core.cogs.logging', # still broken
    'core.cogs.anime',
    'core.cogs.nsfw',
    'core.cogs.commands',
    'core.cogs.fun',
    'core.cogs.math',
    'core.cogs.mod',
    'core.cogs.owner',
    'core.cogs.tags',
    'core.cogs.tasks'
)


TIME = time.time()

class Amaya(Bot):
    """
    Main `class` for the bot to acually run.
    """
    def __init__(self) -> None:
        self._owner = 350750086357057537

        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            intents=Intents.all(),
            owner_id=self._owner)
    

    def _uptime(self) -> Optional[datetime.datetime]:
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
    def fate(self) -> Optional[User]:
        user = self.fetch_user(self._owner)
        return user.id


    async def get_prefix(self, msg: Optional[Message]) -> Optional[str]:
        if not msg.guild:
            return ('a.', 'a!')
        else:
            query = 'SELECT prefix FROM prefixes WHERE id = $1'
            prefix = await self.pool.fetchval(query, msg.guild.id)

            if not prefix:
                return commands.when_mentioned_or('a!', 'a.')(self, msg)
            return commands.when_mentioned_or(prefix)(self, msg)

    async def on_ready(self) -> None:
        self.uptime = int(round(time.time() - TIME))
        print(f"Bot ready. -> {self.user.id}, {self.user.name}")


    async def get_context(self, message, *, cls=None) -> None:
        return await super().get_context(message, cls=Context)

    async def process_commands(self, message) -> None:
        if message.author.bot:
            return
        ctx = await self.get_context(message)

        try:
            if ctx.command is None:
                return
            await self.invoke(ctx)
        finally:
            pass

    async def on_message(self, message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)
               

    async def on_command_error(self, ctx, err) -> None:
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


    def setup(self) -> None:
        print("Loading cogs...")
        for cog in COGS:
            try:
	            self.load_extension(f"{cog}")
	            print(f" Loaded {cog} cog.")
            except Exception:
                print(f'\nFailed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

    def run(self) -> None:
        self.setup()
        print("Running bot...")
        super().run(config.bot_token, reconnect=True)