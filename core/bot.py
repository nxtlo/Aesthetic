from pathlib import Path
import discord
from discord.ext import commands

class MainBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./core/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)



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


    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("??")(bot, msg)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")