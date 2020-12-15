from pathlib import Path
from discord import Intents, Message, Member, __version__
from discord.ext.commands import when_mentioned_or, Bot
from discord.ext import commands
from data import db
from sqlite3 import OperationalError
from time import sleep
from core.cogs.commands import FetchedUser
from data import config
from core.ext.utils import color

import discord
import io
import os
import copy
import logging
import warnings
import re
import traceback
import sys

log = logging.getLogger(__name__)

def get_prefix(bot, msg: Message):
	_get_prefix = db.field("SELECT prefix FROM Guilds WHERE id = ?", msg.guild.id)
	return when_mentioned_or(_get_prefix)(bot, msg.id)

class Amaya(Bot):
    """
    Main `class` for the bot to acually run.
    """
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./core/cogs/*.py")]
        self._owner = 350750086357057537 # Replace this with your Discord ID

        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            intents=Intents.all(),
            owner_id=self._owner)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")
        print('Logged in as:\n')
        print('Bot name:\n', self.user.name)
        print('Bot id:\n',self.user.id)
        print('Discord Version:\n', __version__)
        print('------')
        print(log)
        for server in self.guilds:
            try:
                db.con.execute("INSERT OR IGNORE INTO owners VALUES (?)", (self._owner,))
                db.con.commit()
            except OperationalError:
                raise

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
        else:
            pass

    def setup(self):
        print("Loading cogs...")

        for cog in self._cogs:
            try:
	            self.load_extension(f"core.cogs.{cog}")
	            print(f" Loaded {cog} cog.")
            except Exception as e:
                print(f'\nFailed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

        print("\n Connecting to database....")
        if os.path.exists("./database/database.db"):
            if io.open_code("./database/sqhema.sql"):
                sleep(1)
                print(" Database connected.\n")
        else:
            warnings.simplefilter("always")
            warnings.warn("Database not connected!")

    def run(self):
        self.setup()
        print("Running bot...")
        super().run(config.bot_token, reconnect=True)
