"""
The backend for the bot
"""
from data import db
from discord.ext.commands import command, is_owner, Cog, has_permissions, guild_only, bot_has_permissions, group
from discord.ext import commands
from discord import Embed
from datetime import datetime
from time import strftime
from core.ext.utils import color
import asyncio
import typing
import logging
import sqlite3
import discord

class Database(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._log_channel = 512946130691162112
        self.default_prefix = "ae>"
        self._logger = logging.getLogger(__name__)
    
    def db_update(self):
        db.multiexec("INSERT OR IGNORE INTO Guilds (id) VALUES (?)", ((guild.id,) for guild in self.guild))
        db.con.commit()

    @group(hidden=True)
    async def db(self, ctx):
        pass

    @db.command(name="help")
    async def db_help(self, ctx):
        e = Embed(
            title="Database commands.",
            description="`init`: initializes the bot to the database\n "
                        "`info`: gives info about the database system\n "
                        "`SELECT`: returns anything from the database",
            color=color.invis(self)
        )
        await ctx.send(embed=e)


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
        except Exception:
            raise self._logger
    
    @db.command("SELECT", aliases=['select'])
    @is_owner()
    async def select_db(self, ctx, option: str, from_table: str, coloumn: str, *, inp=None) -> list:
        
        def _all():
            all_guilds = inp or ctx.guild.id
            snowflake = db.cur.execute(f"SELECT {option} FROM {from_table} WHERE {coloumn} = ?", (all_guilds,))

            for table in snowflake.fetchall():
                return "\n".join(map(str, table))
        try:
            e = Embed(color=color.invis(self))
            e.add_field(name="Table name:" ,value=f'```{from_table}```', inline=False)
            e.add_field(name="Resaults:", value=format(_all()), inline=False)
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(e)
        
    
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
    bot.add_cog(Database(bot))