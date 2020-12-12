from pathlib import Path
from discord import Intents, Message, Member
from discord.ext.commands import when_mentioned_or, Bot
from data import db
from sqlite3 import OperationalError
from time import sleep
from core.cogs.commands import FetchedUser

<<<<<<< HEAD
OWNERID = 350750086357057537
=======
import io
import os
import copy
import logging
import warnings
import re
>>>>>>> ab319af95de7c20e10659af729e11a8048f5768c

log = logging.getLogger(__name__)

def get_prefix(bot, msg: Message):
	_get_prefix = db.field("SELECT prefix FROM Guilds WHERE id = ?", msg.guild.id)
	return when_mentioned_or(_get_prefix)(bot, msg.id)

class Aesthetic(Bot):
    """
    Main `class` for the bot to acually run.
    """
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./core/cogs/*.py")]
        self._owner = 350750086357057537
        
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            intents=Intents.all(),
<<<<<<< HEAD
            owner_id=OWNERID)
=======
            owner_id=self._owner)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")
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
>>>>>>> ab319af95de7c20e10659af729e11a8048f5768c

    def setup(self):
        print("Loading cogs...")

        for cog in self._cogs:
            self.load_extension(f"core.cogs.{cog}")
            print(f" Loaded {cog} cog.")
        
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
        with open("data/token.0", "r",encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)