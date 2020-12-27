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
from data import config
#--------------
import requests
import mystbin
import subprocess
import asyncio
import logging
import discord
import texttable


class Sql(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._log_channel = 789614938247266305
        self._logger = logging.getLogger(__name__)
        self._mystbin = mystbin.Client(session=requests.Session())
        self.table = texttable.Texttable()

    @group(hidden=True)
    async def db(self, ctx):
        """Commands for returning stuff from the database"""
        pass

    @db.command(name="table", aliases=['tbl'], hidden=True)
    @is_owner()
    async def _pragma(self, ctx, *, table: str):
        """
        Format the table and render it as rST format
        """
        try:
            async with ctx.typing():
                cmd = f'psql -U {config.db_user} -d {config.database} -c "\d {table}"'
                result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if table:
                    if len(cmd) < 2000:
                        await ctx.send(f"```\n{result.communicate()[0]}\n```")
                    else:
                        content = self._mystbin.post(f"{result.communicate()[0]}", syntax='sql').url
                        return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        except Exception:
            raise
        finally:
            pass

    @db.command(name="schema", hidden=True)
    @is_owner()
    async def _schema(self, ctx):
        """Show the database schema"""
        try:
            async with ctx.typing():
                cmd = f'psql {config.db_user} {config.database} -c "\dt"'
                schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    e = Embed(description=f"```sql\n{schema.communicate()[0]}\n```")
                    await ctx.send(embed=e)
                elif len(cmd) > 2000:
                    content = self._mystbin.post(f"{schema.communicate()[0]}", syntax='sql').url
                    return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        except Exception as e:
            raise e
    
    @db.command(name="rows", hidden=True)
    @is_owner()
    async def _rows(self, ctx, *, column: str):
        """View table rows"""
        try:
            async with ctx.typing():
                cmd = f'psql {config.db_user} {config.database} -c "SELECT * FROM {column};"'
                schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    e = Embed(description=f"```sql\n{schema.communicate()[0]}\n```")
                    await ctx.send(embed=e)
                elif len(cmd) > 2000:
                    content = self._mystbin.post(f"{schema.communicate()[0]}", syntax='sql').url
                    return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        except Exception as e:
            raise e

    
    @db.command(name='grab', hidden=True)
    @is_owner()
    async def _select(self, ctx, option, *, table):
        """Select content from a table"""
        try:
            if not table in self.bot.pool.tables:
                return await ctx.send("Couldn't find the table")
            else:
                content = await self.bot.pool.tables[table].select(option)

                fmt = "".join(str(content).replace("{","").replace("}", "").replace("'content': ", "").replace("'", "").replace("'", "")).replace("[", "").replace("]", "").replace(",", "\n")
                final = f'```\n{fmt}\n```'
                e = Embed(description=final)
                await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(e)


    @db.command(name="new", aliases=['crt'], hidden=True)
    @is_owner()
    async def cr_tbl(
                    self, 
                    ctx, 
                    name, 
                    col1 = None, 
                    type1 = None, 
                    col2 = None, 
                    type2 = None, 
                    col3 = None, 
                    type3 = None, 
                    pkey = None
                    ):
        """
        Create database tables from discord.
        Limit is 3 coloumns.
        """
        try:
            if not name in self.bot.pool.tables:
                await self.bot.pool.create_table(
                    name,
                    [
                        (col1, type1),
                        (col2, type2),
                        (col3, type3)
                    ],
                    prim_key=pkey
                )
                await asyncio.sleep(2)
                await ctx.send("Done!")
            else:
                await ctx.send("Table is already in the database.")
        except Exception as e:
            await ctx.send(e)

    @command(name="format", hidden=True)
    @is_owner()
    async def _format(self, ctx, *, member: discord.Member=None):
        """Testing a rst table format with textable"""
        
        member = member or ctx.author
        if member is not None:
            self.table.set_cols_align(["l", "r", "c"])
            self.table.set_cols_valign(["t", "m", "b"])
            self.table.add_rows([
                [
                    "Member",
                    "Discriminator ",
                    "JoinedAt"
                ],
                [
                    member.name,
                    member.discriminator,
                    member.joined_at
                ]
            ])
            fmt = self.table.draw()
            e = Embed(description=f"```\n{fmt}\n```")
            await ctx.send(embed=e)
        else:
            self.table.set_cols_align(["l", "r", "c"])
            self.table.set_cols_valign(["t", "m", "b"])
            self.table.add_rows([
                [
                    "Member",
                    "ID",
                    "JoinedAt"
                ],
                [
                    member.name,
                    member.id,
                    member.joined_at
                ]
            ])
            fmt = self.table.draw()
            e = Embed(description=f"```\n{fmt}\n```")
            await ctx.send(embed=e)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        roles = [role.mention for role in guild.roles]
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
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 20 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.bot.get_channel(self._log_channel)
        await chan.send(embed=e)
        print(f"Bot joined {guild.name} at {datetime.utcnow()}")



    @Cog.listener()
    async def on_guild_remove(self, guild):
        roles = [role.mention for role in guild.roles]
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
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 20 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.bot.get_channel(self._log_channel)
        await chan.send(embed=e)
        print(f"Bot left {guild.name} at {datetime.utcnow()}")

def setup(bot):
    bot.add_cog(Sql(bot))