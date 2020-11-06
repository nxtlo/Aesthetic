from data import db as d
from discord.ext.commands import command, is_owner, Cog, has_permissions, guild_only, bot_has_permissions
from discord.ext import commands
from discord import Embed
from datetime import datetime
from time import strftime
import discord





class Database(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        print("Data base connected")
        return


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

    # automatically adds the guilds to the database with its info


    @Cog.listener()
    async def on_guild_join(self, guild):
        
        d.cur.execute("SELECT * FROM Guilds WHERE id = ?", (guild.id,))

        res = d.cur.fetchone()
        if res:
            d.cur.execute("UPDATE * FROM Guilds WHERE id = ?")
        else:
            d.cur.execute("INSERT INTO Guilds VALUES (?,?,?,?,?)",
                (guild.id, 
                guild.name, 
                guild.owner_id,
                guild.member_count,
                guild.me.joined_at))
            d.con.commit()

    @Cog.listener()
    async def on_guild_remove(self, member):
        pass


def setup(bot):
    bot.add_cog(Database(bot))