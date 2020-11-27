import discord
from discord.ext import commands
from data import db
import datetime
from discord import Status
from typing import Union
from core.cogs.commands import FetchedUser
from core.ext.utils import emojis as emj

class User(commands.Cog, name="\U0001f464 User"):
    def __init__(self, bot):
        self.bot = bot


# From R.Danny for info command with some addition by me
    

    @commands.command(name="info")
    async def user_info(self, ctx, *, user: Union[discord.Member, FetchedUser] = None):
        """Show user info"""
        user = user or ctx.author
        e = discord.Embed()
        e.color = ctx.author.color
        roles = [role.name.replace('@', '@\u200b') for role in getattr(user, 'roles', [])]
        
        mob = user.is_on_mobile()
        custom_stats = user.activity
        booster = user.premium_since

        online = Status.online
        dnd = Status.dnd
        idle = Status.idle
        offline = Status.offline

        e.add_field(name=f"{emj.mem(self)} ID", value=user.id, inline=False)
        e.add_field(name=f"{emj.plus(self)} Joined server at", value=user.joined_at, inline=False)
        e.add_field(name=f"{emj.dscord(self)} Created account",value=user.created_at, inline=False)
        
        if booster:
            e.add_field(name=f"{emj.boost(self)} Booster since", value=user.premium_since, inline=False)
        if mob:
            e.add_field(name="<:phone:779159717388877846> Is on Mobile", value=mob, inline=False)
        if custom_stats:
            e.add_field(name=f"{emj.custom_status(self)} Custom Status", value=user.activity, inline=False)
        
        if user.status == online:
            e.add_field(name="Status", value=f"{emj.online(self)} {user.status}")
        
        elif user.status == dnd:
            e.add_field(name="Status", value=f"{emj.dnd(self)} {user.status}")
        
        elif user.status == idle:
            e.add_field(name="Status", value=f"{emj.idle(self)} {user.status}")
        
        elif user.status == offline:
            e.add_field(name="Status", value=f"{emj.offline(self)} {user.status}")

        e.add_field(name=f'{emj.setting(self)} Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles', inline=False)
        e.set_author(name=str(user))
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(User(bot))