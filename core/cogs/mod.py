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
    async def ban(self, ctx, member: Union[Member, FetchedUser], *, reason: Optional[str] = 'No reason.'):
        """
        Bans a member from the guild.
        """
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


    @command(name="unban")
    @has_guild_permissions(ban_members=True)
    @bot_has_guild_permissions(ban_members=True)
    @guild_only()
    async def unban_command(self, ctx, member: Union[Member, FetchedUser], *, reason: Optional[str] = 'No reason.'):
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


    @group(invoke_without_command=True)
    @guild_only()
    @check.admin_or_permissions(manage_guild=True)
    async def warn(self, ctx, member: Union[Member, FetchedUser], *, reason: Optional[str]=None):
        """
        Warn a member by their name or id.
        You will need the admin or `manage_guild` perms to use this command.
        ```Usage: warn <@member/id> <reason>```
        """
        try:
            if member.id == self.bot.fate or member.id == ctx.author.id:
                return
            if not reason:
                    return await ctx.send(f"a reason is required.")
            else:
                query = '''
                        INSERT INTO warns(guild_id, warn_id, author_id, member_id, reason, warned_at)
                        VALUES($1, $2, $3, $4, $5, $6)
                        '''
                await self.bot.pool.execute(query, ctx.guild.id, str(uuid4())[:8], ctx.author.id, member.id, reason, ctx.message.created_at)
                await ctx.send(f"Warned {member.mention} for {reason}")
        except Exception as e:
            raise e

    @warn.error
    async def _warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to warn.")


    @warn.command(name='remove', aliases=['del'], usage='')
    @guild_only()
    @check.admin_or_permissions(manage_guild=True)
    async def _del_warn(self, ctx, *, warn_id: str):
        '''
        Delete a member's warn
        ```Usage: warn remove <@member/id> <warn_id>```
        if you don't know the warm id just type warns @member
        '''
        _check = await self.bot.pool.fetch("SELECT warn_id FROM warns WHERE guild_id = $1 AND warn_id = $2", ctx.guild.id, warn_id)
        if _check:
            await self.bot.pool.execute("DELETE FROM warns WHERE warn_id = $1 AND guild_id = $2", warn_id, ctx.guild.id)
            await ctx.send("Warn removed.")
        else:
            await ctx.send("Couldn't find that id.")


    @warn.command(name='info')
    @guild_only()
    @check.admin_or_permissions(manage_guild=True)
    async def _warn_info(self, ctx, *, warn_id: str):
        '''
        info about a warn by its ID
        if you don't know the warm id just type warns @member
        '''
        if not warn_id:
            await ctx.send('No warn id was provided.')

        else:
            found = await self.bot.pool.fetch("SELECT * FROM warns WHERE warn_id = $1 AND guild_id = $2", warn_id, ctx.guild.id)
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
                    e.add_field(name='Warned at', value=warn['warned_at'])
                    await ctx.send(embed=e)
            else:
                await ctx.send("No warns found.")


    @command()
    @guild_only()
    @check.admin_or_permissions(manage_guild=True)
    async def warns(self, ctx, member: Union[Member, FetchedUser]= None):
        '''
        Show a member's warns.
        You will need the admin or `manage_guild` perms to use this command.
        ```Usage: warns <member_id> or <member name> or <@member>```
        '''
        if not member:
            return await ctx.send(f"{member.name} has no warns.")
        else:
            found = await self.bot.pool.fetch("SELECT * FROM warns WHERE member_id = $1 AND guild_id = $2", member.id, ctx.guild.id)
            if found:
                fmt = '\n'.join(r['reason'] + ' ' + f"(ID: {r['warn_id']})" for r in found)
                '''pages = Pages(title='Warns', color=color.invis(self), embed=True, timeout=90, use_defaults=True,
                        entries=[fmt], length=10)'''
                e = Embed(color=color.invis(self), description=fmt)
                e.set_author(name=member.display_name, icon_url=member.avatar_url)
                '''await pages.start(ctx)'''
                await ctx.send(embed=e)
            else:
                await ctx.send("No warns found.")


    @command(name="kick")
    @has_guild_permissions(kick_members=True)
    @bot_has_guild_permissions(kick_members=True)
    @guild_only()
    async def kick_command(self, ctx, member: Union[Member, FetchedUser], *, reason: Optional[str] = 'No reason.'):
        """
        kicks a member from the guild.
        """
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

    @command(name="clean", aliases=["purge", "del", "clear"], useage="clean <ammount>")
    @guild_only()
    @has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx, amount: int = 4):
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

    async def on_guild_join(self, guild: discord.Guild):
        roles = [role.mention for role in guild.roles]
        e = discord.Embed(
            title="Joined a new server!",
            color=color.invis(self),
            timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="Server name", value=guild.name)
        e.add_field(name='Server ID', value=guild.id)
        e.add_field(name="Server Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        e.add_field(name="Server region", value=guild.region)
        e.add_field(name="Boosters", value=guild.premium_subscription_count)
        e.add_field(name="Boost Level", value=guild.premium_tier)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 20 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.bot.get_channel(self.bot._log_channel)
        await chan.send(embed=e)

    async def on_guild_remove(self, guild):
        roles = [role.mention for role in guild.roles]
        e = discord.Embed(
            title="Left a server!",
            color=color.invis(self),
            timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="Server name", value=guild.name)
        e.add_field(name='Server ID', value=guild.id)
        e.add_field(name="Server Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        e.add_field(name="Server region", value=guild.region)
        e.add_field(name="Boosters", value=guild.premium_subscription_count)
        e.add_field(name="Boost Level", value=guild.premium_tier)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 20 else f'{len(roles)} roles')
        e.set_thumbnail(url=guild.icon_url)
        chan = self.bot.get_channel(self.bot._log_channel)
        await chan.send(embed=e)


def setup(bot):
    bot.add_cog(Moderation(bot))