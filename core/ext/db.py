import asyncpg
import colorama
import discord
import copy
from discord.ext import commands
from data import config
from typing import Optional

try:
    colorama.init()
except Exception:
    colorama.reinit()
else:
    pass

class PgPool:
    """Base database class."""
    @classmethod
    def copy(cls):
        return copy.copy(cls)

    @classmethod
    async def __ainit__(cls):
        cls._pool = await asyncpg.create_pool(
            user = config.db_user,
            password = config.password,
            database = config.database,
            host = config.host,
            port = config.port
        )

        with open('./data/schema.sql', 'r') as sch:
            await cls._pool.execute(sch.read())
        return cls._pool