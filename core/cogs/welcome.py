import discord
from random import randint
from discord.ext.commands import command, Cog, group
from discord import Embed
from core.ext import check
from data import db
import datetime



class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_member_join(self, member):
        time = datetime.datetime.utcnow()
        no_bots = len([m for m in member.guild.members if not m.bot])
        with_bots = len(list(member.guild.members))

        e = Embed(
            title=f"Member {member.name} has joined the server!",
            description=f"Welcome to **{member.guild}**! You are the `{no_bots}` member!\nFor help type `??help`",
            color=randint(0, 0xFFFFFF)
        )
        e.set_thumbnail(url=f"{member.avatar_url}")
        e.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        e.set_footer(text=f"{self.bot.user.name}", icon_url=f"{self.bot.user.avatar_url}")
        e.timestamp = time
        channel = self.bot.get_channel(id=512946130691162112)
        await channel.send(embed=e)

    
    @Cog.listener()
    async def on_member_remove(self, member):
        pass


        # this still needs to be worked on

    
    @group(invoke_without_command=True)
    @check.is_mod()
    async def welcome(self, ctx):
        """
        Welcome message
        """
        e = Embed(
            title="Welcome command.",
            description="Set member welcome message.\n\nChannel Setup: welcome channel **<channel>** to set the main channel.\n\nSample: you can type `welcome sample` how it looks"
        )
        await ctx.send(embed=e)
    

    @welcome.command(name="channel")
    @check.is_mod()
    async def channel_command(self, ctx, chan: discord.TextChannel):

        db.cur.execute(f"SELECT channel_id FROM welcomes WHERE guild_id = {ctx.guild.id}")
        res = db.cur.fetchone()
            
        if res:
            insert = ("UPDATE welcomes SET msg = ? WHERE guild_id = ?")
            values = (ctx.guild.id, chan.id, ctx.author.id)
            
            e = Embed(
                description=f"Welcoming Channel has been updated to {chan.mention}",
                color = ctx.author.color
            )
            await ctx.send(embed=e)
        else:
            insert = ("INSERT INTO welcomes(guild_id, channel_id, msg_setter) VALUES (?,?,?)")
            values = (ctx.guild.id, chan.id, ctx.author.id)
            
            e = Embed(
                description=f"Welcoming Channel has been set to {chan.mention}",
                color = ctx.author.color
            )
            await ctx.send(embed=e)
            
            db.cur.execute(insert, values)
            db.commit()
            db.cur.close()
            db.close()

    @welcome.command(name="sample")
    @check.is_mod()
    async def welcome_sample(self, ctx):
        time = datetime.datetime.utcnow()

        e = Embed(
            title=f"Member Fate 怒 has joined the server!",
            description=f"Welcome to **{ctx.guild.name}**! You are the `6969` member!\nFor help type `??help`",
            color=randint(0, 0xFFFFFF)
        )
        e.set_thumbnail(url=f"{ctx.author.avatar_url}")
        e.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
        e.set_footer(text=f"{self.bot.user.name}", icon_url=f"{self.bot.user.avatar_url}")
        e.timestamp = time
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Welcome(bot))