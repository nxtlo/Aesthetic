from discord.ext.commands import Cog, command, group
from discord import Embed, TextChannel, Member
from ..ext.utils import color
from datetime import datetime
from ..ext import check
from typing import Optional
from discord import abc
import discord


class Logging(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group()
    async def log(self, ctx):
        '''Setup the logging'''


    async def exists(self, where: Optional[int]):
        '''Fetches the logging table and returns the channel id'''
        try:
            query = '''
                    SELECT logchannel
                    FROM logging
                    WHERE guild_id = $1
                    '''
            return await self.bot.pool.fetch(query, where)
        except Exception:
            pass


    async def update(self, chanid: Optional[int], guildid: Optional[int]) -> None:
        '''Updates the channel id'''
        try:
            if chanid and guildid:
                query = '''
                        UPDATE logging 
                        SET logchannel = $1 
                        WHERE guild_id = $2
                        '''
                executed = await self.bot.pool.execute(query, chanid, guildid)
                return executed
            return None
        except Exception:
            pass


    async def insert(self, cid: int, gid: int) -> None:
        '''Inserts the channel id'''
        try:
            if cid and gid:
                query = '''
                        INSERT INTO logging(guild_id, logchannel) 
                        VALUES($1, $2)
                        '''
                executed = await self.bot.pool.execute(query, gid, cid)
                return executed
            return None
        except Exception:
            pass

    
    async def wrapchan(self, cid: int):
        if not cid:
            return
        else:
            query = '''
                    SELECT logchannel 
                    FROM logging 
                    WHERE guild_id = $1
                    '''
            fetched = await self.bot.pool.fetchval(query, cid)
            try:
                return fetched
            except:
                pass


    @log.command(name='channel', aliases=['chan'])
    @check.admin_or_permissions(manage_guild=True)
    async def chan(self, ctx, channel: Optional[TextChannel] = None):
        '''All possible logging will be sent to the specified channel.'''

        if not channel:
            await ctx.send("Please mention a channel.")

        if not await self.exists(ctx.guild.id):
            await self.insert(cid=channel.id, gid=ctx.guild.id)
            await ctx.send(f"Logging channel set to {channel.mention}")
        else:
            await self.update(chanid=channel.id, guildid=ctx.guild.id)
            await ctx.send(f"Logging channel updated to {channel.mention}")



    
    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", before.guild.id)
        if channel:
            chan = self.bot.get_channel(id=int(channel))
            e = Embed(description=f"{before.mention} was Updated.", timestamp=datetime.utcnow())

            if before.display_name != after.display_name:

                e.set_author(name=before.display_name, icon_url=before.avatar_url)
                e.add_field(name=f"Was", value=before.display_name, inline=False)
                e.add_field(name="Now", value=after.display_name)

            if before.roles != after.roles:
                bef = [r.mention for r in before.roles]
                af = [r.mention for r in after.roles]
                e.set_author(name=before.display_name, icon_url=before.avatar_url)
                e.set_thumbnail(url=after.avatar_url)
                e.add_field(name="User ID", value=before.id)
                e.add_field(name="Was", value=', '.join(bef), inline=False)
                e.add_field(name="Now", value=', '.join(af))

            '''if before.avatar_url != after.avatar_url:
                e = Embed(description=f"{before.mention} Changed their avatar.")
                e.timestamp=datetime.utcnow()
                e.set_author(name=before.display_name)
                e.set_thumbnail(name=f"Was", value=before.avatar_url, inline=False)
                e.set_image(name="Now", value=after.avatar_url)
                await chan.send(embed=e)'''

            if before.guild_permissions != after.guild_permissions:
                _bef = '\n'.join(perm for perm, value in before.guild_permissions if value)
                _aft = '\n'.join(perm for perm, value in after.guild_permissions if value)
                e.set_author(name=before.display_name, icon_url=before.avatar_url)
                e.add_field(name="User ID", value=before.id)
                e.add_field(name="Was", value=_bef, inline=False)
                e.add_field(name="Now", value=_aft)

            if before.status != after.status:
                return

            if before.activity != after.activity:
                return

            if before.activities != after.activities:
                return

            await chan.send(embed=e)
        else:
            pass

    @Cog.listener()
    async def on_message_edit(self, before, after):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", before.guild.id)
        if channel:
            chan = self.bot.get_channel(id=int(channel))
            e = Embed(description=f"a [Message]({before.jump_url}) has been deleted by {before.author.mention}", timestamp=datetime.utcnow())
            e.set_author(name=before.author.display_name, icon_url=before.author.avatar_url)
            e.add_field(name='Edited at', value=before.channel.mention)
            e.add_field(name='Message ID', value=before.id)
            e.add_field(name="Was", value=before.clean_content, inline=False)
            e.add_field(name='Now', value=after.clean_content)
            await chan.send(embed=e)
        else:
            return



    @Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", member.guild.id)
        if channel:
            chan = self.bot.get_channel(id=int(channel))
            e = Embed(description=f"Member {member.mention} has joined the server!", timestamp=datetime.utcnow())
            e.set_author(name=member.display_name, icon_url=member.avatar_url)
            e.set_thumbnail(url=member.avatar_url)
            e.add_field(name="Joining date", value=member.joined_at, inline=False)
            e.add_field(name="Member Count", value=len(member.guild.members), inline=False)
            e.add_field(name="Roles", value=", ".join([role.mention for role in getattr(member, 'roles', [])]), inline=False)
            await chan.send(embed=e)
        else:
            return


    @Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", member.guild.id)
        if channel:
            chan = self.bot.get_channel(id=int(channel))
            e = Embed(description=f"Member {member.mention} has left the server!", timestamp=datetime.utcnow())
            e.set_author(name=member.display_name, icon_url=member.avatar_url)
            e.set_thumbnail(url=member.avatar_url)
            e.add_field(name="Joining date", value=member.joined_at, inline=False)
            e.add_field(name="Leaving date", value=datetime.utcnow(), inline=False)
            e.add_field(name="Member Count", value=len(member.guild.members), inline=False)
            e.add_field(name="Roles", value=", ".join([role.mention for role in getattr(member, 'roles', [])]), inline=False)
            await chan.send(embed=e)
        else:
            return


    @Cog.listener()
    async def on_guild_channel_update(self, before: abc.GuildChannel, after: abc.GuildChannel):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", before.guild.id)
        if channel:
            chan = self.bot.get_channel(id=int(channel))
            
            e = Embed(description=f"Channel {before.name} has been updated!", timestamp=datetime.utcnow())
            
            if before.name != after.name:
                e.add_field(name='Name was', value=before.name)
                e.add_field(name='Now', value=after.name)
            
            if before.category != after.category:
                e.add_field(name='Category was', value=before.category)
                e.add_field(name='Moved to', value=after.category)
            
            if before.changed_roles != after.changed_roles:
                e.add_field(name="Roles was", value=before.changed_roles)
                e.add_field(name="Roles now", value=after.changed_roles)
            
            if before.topic != after.topic:
                e.add_field(name="Topic was", value=before.topic)
                e.add_field(name="Topic now", value=after.topic)
            
            
            if before.members != after.members:
                e.add_field(name='Members was', value=before.members)
                e.add_field(name='Members now', value=after.members)
            await chan.send(embed=e)

    @Cog.listener()
    async def on_guild_channel_create(self, cn: abc.GuildChannel):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", cn.guild.id)
        if channel:
            chan = self.bot.get_channel(id=int(channel))
            e = Embed(description=f"Channel {cn.name} has been created!", timestamp=datetime.utcnow())
            e.add_field(name='Channel name', value=cn.name, inline=True)
            e.add_field(name='Channel ID', value=cn.id, inline=True)
            e.add_field(name='Channel category', value=cn.category, inline=True)
            await chan.send(embed=e)


    @Cog.listener()
    async def on_guild_channel_remove(self, channel):
        pass

    
    @Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", before.id)
        if channel:
            async for c in before.audit_logs(limit = 1, action = discord.AuditLogAction.guild_update):
                creator = c.user
                chan = self.bot.get_channel(id=int(channel))
                e = Embed(title=f'Guild was updated. by {creator}', timestamp=datetime.utcnow())

                if before.icon != after.icon:
                    e.add_field(name='Icon Changed', value = True)
                    e.set_thumbnail(url=before.icon_url)
                    e.set_image(url=after.icon_url)

                if before.banner != after.banner:
                    e.add_field(name='Banner changed', value = True)
                    e.set_thumbnail(url=before.banner_url)
                    e.set_image(url=after.banner_url)

                if before.region != after.region:
                    e.add_field(name='Region Was', value=before.region, inline=True)
                    e.add_field(name='Region now', value=after.region, inline=True)

                if before.owner != after.owner:
                    e.add_field(name='Owner was', value=before.owner, inline=True)
                    e.add_field(name='Owner now', value=after.owner, inline=True)

                if before.name != after.name:
                    e.add_field(name='Name was', value=before.name, inline=True)
                    e.add_field(name='Name now', value=after.name, inline=True)

                if before.premium_tier != after.premium_tier:
                    e.add_field(name='Nitro tier was', value=before.premium_tier)
                    e.add_field(name='Tier now', value=after.premium_tier)

                if before.features != after.features:
                    e.add_field(name='Features was', value=before.features, inline=True)
                    e.add_field(name='Features now', value=after.features, inline=True)
                await chan.send(embed=e)



                
    @Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", role.guild.id)
        if channel:
            async for c in role.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_create):
                creator = c.user
                chan = self.bot.get_channel(id=int(channel))
                e = Embed(title='New role was created', timestamp=datetime.utcnow())
                e.add_field(name='Crated by', value=creator)
                e.add_field(name='Name', value=role.name, inline=True)
                e.add_field(name='Color', value=role.color, inline=True)
                e.add_field(name='Made by bot?', value=role.is_bot_managed())
                e.add_field(name='Role ID', value=role.id)
                e.add_field(name='Role mention', value=role.mention)
                await chan.send(embed=e)
        else:
            return



    @Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        channel = await self.bot.pool.fetchval("SELECT logchannel FROM logging WHERE guild_id = $1", role.guild.id)
        if channel:
            async for _c in role.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_delete):
                remover = _c.user
                chan = self.bot.get_channel(id=int(channel))
                e = Embed(title='Role was removed', timestamp=datetime.utcnow())
                e.add_field(name='Removed by', value=remover)
                e.add_field(name='Name', value=role.name, inline=True)
                e.add_field(name='Color', value=role.color, inline=True)
                e.add_field(name='Members count', value=len(role.members))
                e.add_field(name='Made by bot?', value=role.is_bot_managed())
                e.add_field(name='Role ID', value=role.id)
                await chan.send(embed=e)
        else:
            return


    @Cog.listener()
    async def on_guild_role_update(self, before, after):
        pass



def setup(bot):
    bot.add_cog(Logging(bot))