from discord.ext.commands import command, is_owner, Cog, has_guild_permissions, guild_only, Converter, Context, group, bot_has_guild_permissions
from discord.ext import commands, buttons
from discord import Embed, Member, Guild, NotFound, TextChannel
from datetime import datetime
from ..ext.utils import color
from ..ext import check
from time import strftime
from discord.utils import get
from typing import Union, Optional
from .commands import FetchedUser
from uuid import uuid4 # for generating a random warn ID
import logging
import asyncio
import discord
import random



class Pages(buttons.Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# '\U000027a1'
    @buttons.button(emoji=None)
    async def left(self, ctx, member):
        return

#'\U00002b05'
    @buttons.button(emoji=None)
    async def right(self, ctx, member):
        return



class Moderation(Cog, name="\U0001f6e0 Moderation"):
    '''Commands for moderation'''
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


    @group(invoke_without_command=True)
    @check.is_mod()
    async def warn(self, ctx, member: Union[Member, FetchedUser], *, reason: Optional[str]=None):
        """
        Warn a member by their name or id.
        You will need the `manage_guild` perms to use this command.
        ```Usage: warn <@member/id> <reason>```
        """
        try:
            if member.id == self.bot.fate or member.id == ctx.author.id:
                return
            if not reason:
                    return await ctx.send(f"a reason is required.")
            else:
                await self.bot.pool.tables['warns'].insert(
                guild_id=str(ctx.guild.id),
                warn_id=str(uuid4())[:8],
                author_id=str(ctx.author.id),
                member_id=str(member.id),
                reason=reason,
                date=str(ctx.message.created_at)
                )
                await ctx.message.add_reaction('\U00002705')
        except Exception as e:
            raise e

    @warn.error
    async def _warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to warn.")


    @warn.command(name='remove', aliases=['del'], usage='')
    @check.is_mod()
    async def _del_warn(self, ctx, *, warn_id: str):
        '''
        Delete a member's warn
        ```Usage: warn remove <@member/id> <warn_id>```
        '''
        _check = await self.bot.pool.tables['warns'].select(
            'warn_id',
            where={
                'warn_id': warn_id,
                'guild_id': ctx.guild.id
            }
        )
        if _check:
            await self.bot.pool.tables['warns'].delete(
                where={
                    'warn_id': warn_id,
                    'guild_id': ctx.guild.id
                }
            )
            await ctx.send("Warn removed.")
        else:
            await ctx.send("Couldn't find that id.")


    @warn.command(name='info')
    @check.is_mod()
    async def _warn_info(self, ctx, *, warn_id: str):
        '''info about a warn by its ID'''
        
        if not warn_id:
            await ctx.send('No warn id was provided.')

        else:
            found = await self.bot.pool.tables['warns'].select(
                '*',
                where={
                    'guild_id': ctx.guild.id,
                    'warn_id': warn_id
                }
            )
            if found:
                for warn in found:
                    
                    reason = ''.join(map(str, warn['reason']))
                    warn_id = ''.join(map(str, warn['warn_id']))
                    member_id = f'<@{warn["member_id"]}>'
                    author_id = f'<@{warn["author_id"]}>'

                    e = Embed(color=color.invis(self), description=f'Warn info for {member_id}')
                    e.add_field(name='Warn ID', value=warn_id)
                    e.add_field(name='Warned by', value=author_id, inline=True)
                    e.add_field(name='Reason', value=reason, inline=False)
                    e.add_field(name='Occurred at', value=warn['date'])
                    await ctx.send(embed=e)
            else:
                await ctx.send("No warns found.")


    @command()
    @check.is_mod()
    async def warns(self, ctx, member: Union[Member, FetchedUser]= None):
        '''
        Show a member's warns.
        ```Usage: warns <member_id>```
        '''
        if not member:
            return
        else:
            found = await self.bot.pool.tables['warns'].select(
                '*',
                where={
                    'guild_id': ctx.guild.id,
                    'member_id': member.id
                }
            )
            if found:
                fmt = '\n'.join(r['reason'] + ' ' + f"(ID: {r['warn_id']})" for r in found)
                pages = Pages(title='Warns', color=color.invis(self), embed=True, timeout=90, use_defaults=True,
                        entries=[fmt], length=10)
                e = Embed(color=color.invis(self), description=fmt)
                e.set_author(name=member.display_name, icon_url=member.avatar_url)
                await pages.start(ctx)
                # await ctx.send(embed=e)
            else:
                await ctx.send("No warns found.")


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


    @command(name="clean", aliases=["purge", "del", "clear"], useage="clean <ammount>")
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
    async def leave_guild(self, ctx):
        """Make the bot leave from the guild"""
        try:
            msg = ctx.message
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