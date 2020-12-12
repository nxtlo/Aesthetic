from data import db as d
from discord.ext.commands import command, is_owner, Cog, has_permissions, guild_only, bot_has_permissions, Converter, Context, group
from discord.ext import commands
from discord import Embed, Member, Guild, NotFound, TextChannel
from datetime import datetime
from ..ext.utils import color
from time import strftime
from discord.utils import get
from typing import Union, Optional
from sqlite3 import ProgrammingError
import logging
from .commands import FetchedUser
import asyncio
import discord

class Moderation(Cog, name="\U0001f6e0 Moderation"):
    def __init__(self, bot):
        self.bot = bot


    @command(name="ban")
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @guild_only()
    async def ban(self, ctx, member: Union[Member, FetchedUser], *, reason=None):
        """
        Bans a member from the guild.
        """
        
        foo = d.cur.execute("SELECT * FROM bans WHERE id = ?", (member.id,))

        fetched = foo.fetchone()

        if fetched:
            return await ctx.send(f"Member {member.display_name} is already banned.")
            

        else:
            d.cur.execute("INSERT OR IGNORE INTO bans VALUES (?,?,?,?,?)", (
                member.guild.id,
                member.id,
                ctx.author.id,
                ctx.message.created_at,
                reason))
        d.con.commit()

        try:
            if reason is None:

                null = strftime("%A, %d %Y/%m, %H:%M:%S %p")
                
                e = Embed(
                    title=f"a member has been banned with no reason"
                )
                e.add_field(name=f"Author:", value=f"{ctx.author}\nID:{ctx.author.id}", inline=False)
                e.add_field(name=f"Member:", value=f"{member.name}#{member.discriminator}\nID:{member.id}", inline=False)
                e.add_field(name="Occurred at", value=null, inline=False)
                e.set_thumbnail(url=member.avatar_url)
                await ctx.guild.ban(member)
                await ctx.send(embed=e)
            elif reason:
                null = strftime("%A, %d %Y/%m, %H:%M:%S %p")
                e = Embed(
                    title=f"a member has been banned"
                )
                e.add_field(name=f"Author:", value=f"{ctx.author}\nID:{ctx.author.id}", inline=False)
                e.add_field(name=f"Member:", value=f"{member.name}#{member.discriminator}\nID:{member.id}", inline=False)
                e.add_field(name="Occurred at", value=null, inline=False)
                e.add_field(name="Reason:", value=reason)
                e.set_thumbnail(url=member.avatar_url)
                await ctx.guild.ban(member)
                await ctx.send(embed=e)
            else:
                print(f"{ctx.author.name} tried to ban someone and he doesn't have perms")
                return
        except commands.MissingPermissions as e:
            await ctx.send(e)





    @command(name="unban")
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @guild_only()
    async def unban_command(self, ctx, member: Union[Member, FetchedUser], *, reason=None):
        
        d.cur.execute("DELETE FROM bans WHERE member_id = ?", (member.id,))

        try:
            if reason is None:

                null = strftime("%A, %d %Y/%m, %H:%M:%S %p")
                
                e = Embed(
                    title=f"A member was unbanned with no reason"
                )
                e.add_field(name=f"Author:", value=f"{ctx.author}\nID:{ctx.author.id}", inline=False)
                e.add_field(name=f"Member:", value=f"{member.name}#{member.discriminator}\nID:{member.id}", inline=False)
                e.add_field(name="Occurred at", value=null, inline=False)
                e.set_thumbnail(url=member.avatar_url)
                await ctx.guild.unban(member)
                await ctx.send(embed=e)
            elif reason:
                null = strftime("%A, %d %Y/%m, %H:%M:%S %p")
                e = Embed(
                    title=f"A member has been Unbanned"
                )
                e.add_field(name=f"Author:", value=f"{ctx.author}\nID:{ctx.author.id}", inline=False)
                e.add_field(name=f"Member:", value=f"{member.name}#{member.discriminator}\nID:{member.id}", inline=False)
                e.add_field(name="Occurred at", value=null, inline=False)
                e.add_field(name="Reason:", value=reason)
                e.set_thumbnail(url=member.avatar_url)
                await ctx.guild.unban(member)
                await ctx.send(embed=e)
            else:
                print(f"{ctx.author.name} tried to unban someone and he doesn't have perms")
                return
        except commands.MissingPermissions as e:
            await ctx.send(e)



    @command(name="kick")
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @guild_only()
    async def kick_command(self, ctx, member: Union[Member, FetchedUser], *, reason=None):
        """
        kicks a member from the guild.
        """
        foo = d.cur.execute("SELECT * FROM kicks WHERE id = ?", (member.id,))

        fetched = foo.fetchone()

        if fetched:
            return await ctx.send(f"Member {member.display_name} is already kicked.")

        try:
            if reason is None:

                null = strftime("%A, %d %Y/%m, %H:%M:%S %p")
                
                e = Embed(
                    title=f"a member has been kicked with no reason"
                )
                e.add_field(name=f"Author:", value=f"{ctx.author}\nID:{ctx.author.id}", inline=False)
                e.add_field(name=f"Member:", value=f"{member.name}#{member.discriminator}\nID:{member.id}", inline=False)
                e.add_field(name="Occurred at", value=null, inline=False)
                e.set_thumbnail(url=member.avatar_url)
                await ctx.guild.kick(member)
                await ctx.send(embed=e)
                d.cur.execute("INSERT OR IGNORE INTO kicks VALUES (?,?,?,?,?)", (
                    member.guild.id,
                    member.id,
                    ctx.author.id,
                    ctx.message.created_at))
                d.con.commit()
            elif reason:
                null = strftime("%A, %d %Y/%m, %H:%M:%S %p")
                e = Embed(
                    title=f"a member has been kicked"
                )
                e.add_field(name=f"Author:", value=f"{ctx.author}\nID:{ctx.author.id}", inline=False)
                e.add_field(name=f"Member:", value=f"{member.name}#{member.discriminator}\nID:{member.id}", inline=False)
                e.add_field(name="Occurred at", value=null, inline=False)
                e.add_field(name="Reason:", value=reason)
                e.set_thumbnail(url=member.avatar_url)
                await ctx.guild.kick(member)
                await ctx.send(embed=e)
                
                d.cur.execute("INSERT OR IGNORE INTO kicks VALUES (?,?,?,?,?)", (
                    member.guild.id,
                    member.id,
                    ctx.author.id,
                    ctx.message.created_at,
                    reason))
                d.con.commit()
            else:
                print(f"{ctx.author.name} tried to kick someone and he doesn't have perms")
                return
        except ProgrammingError as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Moderation(bot))