from data import db as d
from discord.ext.commands import command, is_owner, Cog, has_permissions, guild_only, bot_has_permissions
from discord.ext import commands
from discord import Embed
from datetime import datetime
from time import strftime
from core.ext.utils import color
import asyncio
import json
import discord


LOGGINGCHANNEL = 512946130691162112

class Database(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        print("Database connected")
        return

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
        chan = self.bot.get_channel(LOGGINGCHANNEL)
        await chan.send(embed=e)
        
        
        d.cur.execute("SELECT * FROM Guilds WHERE id = ?", (guild.id,))

        res = d.cur.fetchone()
        if res:
            return res
        else:
            d.cur.execute("INSERT INTO Guilds VALUES (?,?,?,?,?)",
                (guild.id, 
                guild.name, 
                guild.owner_id,
                guild.member_count,
                guild.me.joined_at))
            print(f"Bot joined {guild.name} at {guild.me.joined_at}")
            d.con.commit()

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
        chan = self.bot.get_channel(LOGGINGCHANNEL)
        await chan.send(embed=e)

def setup(bot):
    bot.add_cog(Database(bot))