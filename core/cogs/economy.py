import discord
import datetime
import time
import random

import SimpleEconomy as sec
from discord.ext import commands
from discord import utils as u
from data import db
from core.ext import utils as Emj

# <---- this cog still needs a lot of work :) ----> #


sec.Database_dir = "./database/database.db"
sec.default_balance = 0


class Economy(commands.Cog):
    """```BETA```"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Setup the database"""
        await sec.setup_database(sec.Database_dir)



    @commands.command(name="balance", aliases=['bal'])
    async def balance_command(self, ctx):
        """*Show how much money you have*"""

        await sec.user_check(ctx.author.id)
        bal = await sec.get_balance(ctx.author.id)
        e = discord.Embed(
            title=f"*Doxes bank* \U0001f4b8",
            color=ctx.author.color
        )
        emj = u.get(self.bot.emojis, name="cash")
        e.add_field(name="**Balance**", 
                    value=f"You have `{bal}` doxes in your account {emj}",
                    inline=False)
        await ctx.send(embed=e)



    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="add")
    async def add_money(self, ctx, amt: int, *, member: discord.Member):
        """*Add money to members*"""
        await sec.user_check(member.id)
        author = str(ctx.message.author.mention)
        emj = u.get(self.bot.emojis, name="cash")
        e = discord.Embed(
            color=ctx.author.color,
            title=f"Transactions completed!",
            
            description=f"*Doxes has been added {emj}*",
            timestamp=ctx.message.created_at
        )

        full = await sec.get_balance(ctx.author.id)
        
        e.add_field(name="**Sender**", value=author, inline=True)
        e.add_field(name="**Receiver**", value=member.mention, inline=True)
        e.add_field(name="**Amount added**", value=f"`{amt}`", inline=True)
        e.add_field(name="**Total before**", value=f"```{full}```", inline=True)
        e.add_field(name="**New Total**", value=f"```{amt + full}```", inline=True)
        e.set_footer(text=datetime.datetime.now())
        
        await sec.add_balance(userid=member.id, amount=amt)
        msg = await ctx.send(f"***Please wait.... {Emj.emojis.proc(self)}***")
        time.sleep(3)
        await msg.delete()
        await ctx.send(embed=e)




    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="remove", aliases=['rm'])
    async def remove_money(self, ctx, amt: int, *, member: discord.Member):
        """*Remove money from members*"""
        await sec.user_check(member.id)
        author = str(ctx.message.author.mention)
        emj = u.get(self.bot.emojis, name="cash")
        e = discord.Embed(
            color=ctx.author.color,
            title=f"Transactions completed!",
            
            description=f"*Doxes has been removed {emj}*",
            timestamp=ctx.message.created_at
        )
        
        e.add_field(name="**Removed by**", value=author, inline=True)
        e.add_field(name="**From**", value=member.mention, inline=True)
        e.add_field(name="**Amount removed**", value=f"`{amt}`", inline=True)
        e.set_footer(text=datetime.datetime.now())
        
        await sec.remove_balance(userid=member.id, amount=amt)
        msg = await ctx.send(f"***Please wait.... {Emj.emojis.proc(self)}***")
        time.sleep(3)
        await msg.delete()
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Economy(bot))