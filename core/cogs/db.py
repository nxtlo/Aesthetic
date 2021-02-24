"""
Commands for running sql stuff
"""
from discord.ext.commands import is_owner, Cog, group, command
from discord import Embed
from datetime import datetime
from time import strftime
from core.ext.utils import color
from data import config
from .. import Amaya
#--------------
import mystbin
import subprocess
import asyncio
import logging
import discord


class Database(Cog):
    def __init__(self, bot: Amaya):
        self.bot = bot
        self._log_channel = 789614938247266305

    @staticmethod
    def ToJson(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError


    @group(hidden=True, invoked_without_command=True)
    async def db(self, ctx):
        """Commands for returning stuff from the database"""
        pass

    @db.command(name='init', hidden=True)
    @is_owner()
    async def _init_(self, ctx):
        '''
        Init the bot database and creates the tables.
        **THIS COMMAND SHOULD ONLY ONCE AND RUN IN THE MAIN BOT SERVER.**
        '''
        async with ctx.typing():
            query = "INSERT INTO amaya(bot_id, owner_id, guild_id) VALUES($1, $2, $3)"
            with open('./data/schema.sql', 'r', encoding='utf8') as schema:
                async with ctx.pool.acquire() as conn:
                    try:
                        await conn.execute(schema.read())
                        await asyncio.sleep(2)
                        await conn.execute(query, self.bot.user.id, self.bot.owner_id, ctx.author.guild.id)
                        await ctx.send("\U00002705")
                    finally:
                        await ctx.pool.release(conn)


    @db.command(name='sql', aliases=['query', 'sqlx'], hidden=True)
    @is_owner()
    async def run_query(self, ctx, *, query):
        '''runs sql querys.'''
        if not query:
            return
        else:
            reslut = await self.bot.query(query)
            await ctx.send(f"```\n{reslut}\n```")


    @db.command(name="table", aliases=['info'], hidden=True)
    @is_owner()
    async def _pragma(self, ctx, *, table: str):
        """
        Format the table and render it as rST format
        this command access your psql commandline
        """
        try:
            async with ctx.typing():
                cmd = f'psql -U {config.db_user} -d {config.database} -c "\d {table}"'
                result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if table:
                    if len(cmd) < 2000:
                        await ctx.send(f"```\n{result.communicate()[0]}\n```")
        except Exception:
            raise
        finally:
            pass
    
    @db.command(name="schema", hidden=True)
    @is_owner()
    async def _schema(self, ctx):
        """Show the database schema from psql"""
        try:
            async with ctx.typing():
                cmd = f'psql {config.db_user} {config.database} -c "\dt"'
                schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    e = Embed(description=f"```sql\n{schema.communicate()[0]}\n```")
                    await ctx.send(embed=e)
        except Exception as e:
            raise e
    
    @db.command(name="rows", hidden=True)
    @is_owner()
    async def _rows(self, ctx, *, column: str):
        """View table rows from psql"""
        try:
            async with ctx.typing():
                cmd = f'psql {config.db_user} {config.database} -c "SELECT * FROM {column};"'
                rows = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    await ctx.send(f"```sql\n{rows.communicate()[0]}\n```")
        except Exception as e:
            raise e

def setup(bot):
    bot.add_cog(Database(bot))