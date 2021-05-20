import asyncpg
import discord
from data import config
from typing import Optional
class PgPool:
    """Base database class."""
    @classmethod
    async def __ainit__(cls) -> Optional[asyncpg.pool.Pool]:
        cls._pool: asyncpg.pool.Pool = await asyncpg.create_pool(
            user = config.db_user,
            password = config.password,
            database = config.database,
            host = config.host,
            port = config.port
        )

        with open('./data/schema.sql', 'r') as sch:
            await cls._pool.execute(sch.read())
        return cls._pool