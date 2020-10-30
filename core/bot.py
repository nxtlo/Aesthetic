from pathlib import Path
import discord
from discord import Intents
from discord.ext import commands
from data import db

OWNER_IDS = [350750086357057537]

class MainBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./core/cogs/*.py")]
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            intents=Intents.all(),
            owner_ids=OWNER_IDS)

    def setup(self):
        print("Loading cogs...")

        for cog in self._cogs:
            self.load_extension(f"core.cogs.{cog}")
            print(f" Loaded {cog} cog.")

    def run(self):
        self.setup()
        with open("data/token.0", "r",encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)
    
    
    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                        ((guild.id,) for guild in self.guilds))
        db.commit()


    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")

def get_prefix(bot, message):
	_get_prefix = "??"
	return commands.when_mentioned_or(_get_prefix)(bot, message)