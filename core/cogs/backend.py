"""
The backend and database for the bot
"""
from discord.ext.commands import command, is_owner, Cog, has_permissions, guild_only, bot_has_permissions, group
from discord.ext import commands
from discord import Embed, TextChannel
from datetime import datetime
from time import strftime
from core.ext.utils import color
from typing import Optional
from ..ext import check
from ..bot import Amaya
#--------------
import requests
import mystbin
import subprocess
import asyncio
import logging
import discord


class Sql(Cog):
    def __init__(self, bot: Amaya):
        self.bot = bot
        self._log_channel = 789614938247266305
        self._logger = logging.getLogger(__name__)
        self._mystbin = mystbin.Client(session=requests.Session())

    @group(hidden=True)
    async def db(self, ctx):
        """Commands for returning stuff from the database"""
        pass

    @db.command(name="table", aliases=['tbl'], hidden=True)
    @is_owner()
    async def _pragma(self, ctx, *, table: str):
        """
        Format the database and render it as rST format
        """
        try:
            async with ctx.typing():
                cmd = f'psql -U fate -d fate -c "SELECT * FROM {table}"'
                if table:
                    if len(cmd) < 2000:
                        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                        await ctx.send(f"```\n{result.communicate()[0]}\n```")
                    else:
                        if len(cmd) > 2000:
                            content = self._mystbin.post(f"{result.communicate()[0]}", syntax='sql').url
                            return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")
        finally:
            pass

    @db.command(name="schema", hidden=True)
    @is_owner()
    async def _schema(self, ctx):
        """Show the database schema"""
        try:
            async with ctx.typing():
                cmd = 'psql fate fate -c "\dt"'
                schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    await ctx.send(f"```sql\n{schema.communicate()[0]}\n```")
                elif len(cmd) > 2000:
                    content = self._mystbin.post(f"{schema.communicate()[0]}", syntax='sql').url
                    return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]
        e = Embed(
            title="Joined a new server!",
            color=color.invis(self),
            timestamp=datetime.utcnow()
        )
        e.add_field(name="Server name", value=guild.name)
        e.add_field(name="Server Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        e.add_field(name="Server region", value=guild.region)
        e.add_field(name="Boosters", value=guild.premium_subscription_count)
        e.add_field(name="Boost Level", value=guild.premium_tier)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.bot.get_channel(self._log_channel)
        await chan.send(embed=e)
        print(f"Bot joined {guild.name} at {datetime.utcnow()}")



    @Cog.listener()
    async def on_guild_remove(self, guild):
        e = Embed(
            title="Left a server!",
            color=color.invis(self),
            timestamp=datetime.utcnow()
        )
        e.add_field(name="Server name", value=guild.name)
        e.add_field(name="Server Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        e.add_field(name="Server region", value=guild.region)
        e.add_field(name="Boosters", value=guild.premium_subscription_count)
        e.add_field(name="Boost Level", value=guild.premium_tier)
        e.set_thumbnail(url=guild.icon_url)
        chan = self.bot.get_channel(self._log_channel)
        await chan.send(embed=e)
        print(f"Bot left {guild.name} at {datetime.utcnow()}")



    @Cog.listener()

    async def on_ready(self):
        await self.bot.pool.create_table(
            'tags_conn',
            [
                ('id', str),
                ('tag_name', str)
            ],
            prim_key='id',
            foreign_keys={
                'id': {
                    'table': 'tags',
                    'ref': 'guild_id',
                    'mods': 'ON UPDATE CASCADE ON DELETE CASCADE'
                }
            }
        )



def setup(bot):

    bot.add_cog(Sql(bot))

