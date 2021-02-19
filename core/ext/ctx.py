import discord
import datetime
from discord.ext import commands
from functools import wraps
import asyncio
import copy


def native(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await asyncio.sleep(5)
        coro = await func(*args, **kwargs)
        if isinstance(coro, copy.copy(func)):
            return coro
        return wrapper

class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pool = self.bot.pool

    @property
    def pool(self):
        return self._pool

    @property
    def session(self):
        return self.bot.session


    @property
    def time(self):
        return datetime.datetime.utcnow().strftime('%A, %d %Y/%m, %H:%M:%S %p')