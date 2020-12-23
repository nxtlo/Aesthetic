"""
The backend and database for the bot
"""
from data import db
from discord.ext.commands import command, is_owner, Cog, has_permissions, guild_only, bot_has_permissions, group
from discord.ext import commands
from discord import Embed, TextChannel
from datetime import datetime
from time import strftime
from core.ext.utils import color
from typing import Optional
from ..ext import check
#--------------
import requests
import mystbin
import subprocess
import asyncio
import logging
import sqlite3
import discord

class Sql(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._log_channel = 789614938247266305
        self.default_prefix = "a."
        self._logger = logging.getLogger(__name__)
        self._mystbin = mystbin.Client(session=requests.Session())
    
    def db_update(self):
        db.multiexec("INSERT OR IGNORE INTO Guilds (id) VALUES (?)", ((guild.id,) for guild in self.guild))
        db.con.commit()

    @group(hidden=True)
    async def db(self, ctx):
        """Commands for returning stuff from the database"""
        pass


    @db.command(name="init", hidden=True)
    @is_owner()
    async def db_init(self, ctx):
        """initialize the bot to the guild aka add it to the database\nincase it doesn't respond to commands"""
        db.cur.execute("SELECT * FROM Guilds WHERE id = ?", (ctx.guild.id,))

        init = db.cur.fetchall()
        try:
            if init:
                return
            else:
                db.cur.execute("INSERT OR IGNORE INTO Guilds VALUES (?,?,?,?,?,?)",
                    (ctx.guild.id,
                    self.default_prefix,
                    ctx.guild.name, 
                    ctx.guild.owner_id,
                    ctx.guild.member_count,
                    ctx.guild.me.joined_at))
                db.con.commit()
                await ctx.send(":thumbsup:")
                asyncio.sleep(1)
                await ctx.message.delete()
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")
    
    @db.command("SELECT", aliases=['select'])
    @is_owner()
    async def select_db(self, ctx, option: str, from_table: str, coloumn: str, *, inp=None) -> list:
        """
        Select anything from the database
        
        Example: db select prefix Guilds id
        
        This will basically return the `prefix` from `Guilds` table\nwhere the guild `id` is `ctx.guild.id` or `member.guild.id`
        Another Example: db SELECT * bans id
        This one will select everything from bans where id = member.guild.id
        You can get data for other guilds by doing this:\n\ndb select * Guilds id <guild_id>
        """
        
        def _all():
            all_guilds = inp or ctx.guild.id or ctx.message.guild.id
            snowflake = db.cur.execute(f"SELECT {option} FROM {from_table} WHERE {coloumn} = ?", (all_guilds,))

            for table in snowflake.fetchall():
                return "\n".join(map(str, table))
        try:
            e = Embed(color=color.invis(self))
            e.add_field(name="Table name:" ,value=f'```{from_table}```', inline=False)
            e.add_field(name="Resaults:", value=_all(), inline=False)
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")
    
    @db.command(name="pragma", aliases=['pr'])
    @is_owner()
    async def _pragma(self, ctx, table: str, *, encoding=None):
        """
        Format the database and render it as rST format
        
        You use the `-> json` after the table name to convert the pragma to json

        excample: db pragma/pr Guilds -> json
        """
        try:
            async with ctx.typing():
                # json format
                if table is not None and encoding == '-> json':

                    cmd = f'sqlite-utils {db.DB_PATH} "select * from {table}" | python -mjson.tool'
                    schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                    
                    if len(cmd) < 2000:
                        await ctx.send(f"```json\n{schema.communicate()[0]}\n```")
                    
                    elif len(cmd) > 2000:
                        content = self._mystbin.post(f"{schema.communicate()[0]}", syntax='json').url
                        return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
                
                # if encodibg != json then send it as a normal rST format

                else:
                    cmd = f'sqlite-utils {db.DB_PATH} "select * from {table}" --table'
                    if table:
                        if len(cmd) < 2000:
                            pragma = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                            await ctx.send(f"```\n{pragma.communicate()[0]}\n```")
                        else:
                            if len(cmd) > 2000:
                                content = self._mystbin.post(f"{pragma.communicate()[0]}", syntax='sql').url
                                return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")
        finally:
            pass

    @db.command(name="schema")
    @is_owner()
    async def _schema(self, ctx):
        """Show the database schema"""
        try:
            async with ctx.typing():
                cmd = f'sqlite-utils tables {db.DB_PATH} --schema --table'
                schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                
                if len(cmd) < 2000:
                    await ctx.send(f"```sql\n{schema.communicate()[0]}\n```")
                
                elif len(cmd) > 2000:
                    content = self._mystbin.post(f"{schema.communicate()[0]}", syntax='sql').url
                    return await ctx.send(f"Too many results... Uploaded to mystbin -> {content}")
        
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")
            
    @db.command(name="info")
    async def db_info(self, ctx):
        e = Embed(
            color = color.invis(self)
        )
        e.add_field(name="Sqlite3 version:", value=f"{sqlite3.sqlite_version}", inline=False)
        e.add_field(name="Paramstyle:", value=f"{sqlite3.paramstyle}", inline=False)
        e.add_field(name="Thread Level:", value=sqlite3.threadsafety)
        await ctx.send(embed=e)

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
        
        db.cur.execute("SELECT * FROM Guilds WHERE id = ?", (guild.id,))

        res = db.cur.fetchone()
        if res:
            return res
        else:
            db.cur.execute("INSERT INTO Guilds VALUES (?,?,?,?,?,?)",
                (guild.id,
                self.default_prefix,
                guild.name, 
                guild.owner_id,
                guild.member_count,
                guild.me.joined_at))
            db.con.commit()

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

    # you don't really need this listener unless you're not using this bot for a multi-guild

    """
    # automatically adds users in guilds to the database

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        
        d.cur.execute("SELECT * FROM Users WHERE id=?", (member.id,))
        
        res = d.cur.fetchone()
        
        if res:
            return
        else:
            d.cur.execute("INSERT INTO Users VALUES (?,?,?,?)", 
                (member.id, 
                member.created_at, 
                member.name,
                member.joined_at))
            d.con.commit()
    """



def setup(bot):
    bot.add_cog(Sql(bot))