import discord
import sqlite3
from discord.ext import commands
from data import db
from core.ext import utils as u
import datetime
    
class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="register", aliases=['reg'], discription='Register to the database')
    @commands.guild_only()
    async def register_command(self, ctx):
        db.cur.execute("SELECT * FROM users WHERE id=?", (ctx.author.id,))
        
        response = db.cur.fetchone()
        
        if response:
            embed = discord.Embed(
                title=":grey_exclamation: You're already in the database. type `??help` for more info",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)
        else:
            db.cur.execute("INSERT INTO users VALUES (?,?,?,?)",
                (ctx.author.id, 
                ctx.author.name,
                ctx.author.discriminator,
                ctx.author.joined_at))
            db.con.commit()
            uid, name, discriminator, JoinDate = response
            try:
                embed = discord.Embed(
                    title=f":white_check_mark: You have been registered to the database",
                    color=ctx.author.color,
                    timestamp=ctx.message.created_at,
                    thumbnail=ctx.author.avatar_url
                )
                embed.add_field(
                    name=f"Info:",
                    value=f"**UserID:** `{uid}`\n**UserName:** `{name}#{discriminator}`\n**Join Date:** `{JoinDate}`".format(uid, name, discriminator, JoinDate),
                    inline=False
                    
                )
                embed.set_footer(text="Register Date:")
                await ctx.message.delete()
                await ctx.send(embed=embed)
            except Exception:
                raise

def setup(bot):
    bot.add_cog(User(bot))