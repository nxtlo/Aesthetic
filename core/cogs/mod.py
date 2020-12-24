from discord.ext.commands import command, is_owner, Cog, has_guild_permissions, guild_only, Converter, Context, group, bot_has_guild_permissions
from discord.ext import commands
from discord import Embed, Member, Guild, NotFound, TextChannel
from datetime import datetime
from ..ext.utils import color
from ..ext import check
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
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @guild_only()
    async def ban(self, ctx, member: Union[Member, FetchedUser], *, reason=None):
        """
        Bans a member from the guild.
        """
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
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @guild_only()
    async def unban_command(self, ctx, member: Union[Member, FetchedUser], *, reason=None):

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
    @has_guild_permissions(kick_members=True)
    @bot_has_guild_permissions(kick_members=True)
    @guild_only()
    async def kick_command(self, ctx, member: Union[Member, FetchedUser], *, reason=None):
        """
        kicks a member from the guild.
        """
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
            else:
                print(f"{ctx.author.name} tried to kick someone and he doesn't have perms")
                return
        except:
            pass


    @command(name="clean", aliases=["purge", "del"], useage="clean <ammount>")
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx, amount=4):
        """
        Clean chat messages

        if no amount was provided. this command will delete the last 5 messages
        """
        await ctx.channel.purge(limit=amount+1)


    @command(name="leave")
    @guild_only()
    @check.is_mod()
    async def leave_guild(self, ctx, guild: Guild=None):
        """Make the bot leave from the guild"""
        try:
            msg = ctx.message
            if guild is None:
                await msg.add_reaction("\U00002611")
                await ctx.guild.leave()
            return
        except Exception:
            pass

    @commands.command(name='perms', aliases=['permissions'])
    @check.is_mod()
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions."""
        if not member:
            member = ctx.author
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions:', colour=member.colour)

        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value=perms)
        embed.set_footer(text=f'Requested by: {ctx.author}')
        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

def setup(bot):
    bot.add_cog(Moderation(bot))