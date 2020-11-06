import discord
import sqlite3
import datetime, time
import traceback
import pkg_resources
import sys, platform, psutil
from typing import Union
from datetime import timedelta
from discord.ext import commands
from discord import utils as us
from core.ext import utils as u

start_time = time.time()


class FetchedUser(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument.isdigit():
            raise commands.BadArgument('Not a valid user ID.')
        try:
            return await ctx.bot.fetch_user(argument)
        except discord.NotFound:
            raise commands.BadArgument('User not found.') from None
        except discord.HTTPException:
            raise commands.BadArgument('An error occurred while fetching the user.') from None

class Meta(commands.Cog, name="\U0001f587 Meta"):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(name='fate', aliases=['owner'], hidden=True)
    async def owner_command(self, ctx):
        """Info about the bot maker"""

        embed = discord.Embed(
            title="*Fate's social info*",
            color = ctx.author.color,
            timestamp =ctx.message.created_at,
        )
        embed.add_field(
            name=f"{u.emojis.insta(self)} ```Instagram```", 
            value=u.url.insta, inline=True)

        embed.add_field(
            name=f"{u.emojis.twitter(self)} ```Twitter```", 
            value=u.url.twitter, inline=True)

        embed.add_field(
            name=f"{u.emojis.youtube(self)} ```Youtube```", 
            value=u.url.youtube, inline=True)

        embed.add_field(
            name=f"{u.emojis.steam(self)} ```Steam```", 
            value=u.url.steam, inline=True)

        embed.add_field(
            name=f"{u.emojis.github(self)} ```Github```", 
            value=u.url.github, inline=True)

        embed.add_field(
            name=f"{u.emojis.github(self)} ```Bungie```", 
            value=u.url.bungie)

        embed.set_author(
            name=f"{self.bot.user.name}", 
            icon_url=self.bot.user.avatar_url)
            
        embed.set_footer(text=f"Requested {ctx.author}")
        await ctx.send(embed=embed)

    
    @commands.command(name="invite", usage="invite")
    async def invite(self, ctx):
        """
        Invite this bot
        """
        await ctx.send(
            embed=discord.Embed(
                title="Invite Link",
                description=f"https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}"
                    "&permissions=268823640&scope=bot",
                colour=ctx.author.colour,
                )
            )
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("hi"):
            try:
                await message.channel.send("sup :sunglasses:")
            except:
                pass


    @commands.command(name="status")
    async def status_command(self, ctx, member: discord.Member):
        """Display member's status"""
        if member:
            try:
                e = discord.Embed(
                    description=f"The member {member.mention}' status is `{member.status}`",
                    color=ctx.author.color
                )
                await ctx.send(embed=e)
            except Exception as e:
                await ctx.send(e)
        if not member:
            try:
                e = discord.Embed(
                    description=f"Your status is `{member.status}`",
                    color=ctx.author.color
                )
                await ctx.send(embed=e)
            except Exception as e:
                await ctx.send(e)


    # this command is yoinked from https://github.com/Rapptz/RoboDanny/ with more stuff added by me



    @commands.command(name="botinfo")
    async def about(self, ctx):
        """Tells you information about the bot itself."""

        embed = discord.Embed(
        color=ctx.author.color)
        embed.title=f'{u.emojis.proc(self)} Info about {self.bot.user.name}'

        owner = "Fate ?#5957"
        embed.set_author(name=str(owner), icon_url=self.bot.user.avatar_url)

        # statistics
        total_members = 0
        total_unique = len(self.bot.users)

        text = 0
        voice = 0
        guilds = 0
        for guild in self.bot.guilds:
            guilds += 1
            total_members += guild.member_count
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1
                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1


        
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        os_name = platform.system()
        os_release = platform.release()
        version = pkg_resources.get_distribution('discord.py').version

        embed.add_field(name='Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='Channels', value=f'{text + voice} total\n{text} text\n{voice} voice')
        embed.add_field(name='Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='Guilds', value=guilds)
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')
        embed.add_field(name="VM OS", value=os_name + os_release)
        embed.set_footer(text=f'Made with discord.py v{version}', icon_url='http://i.imgur.com/5BFecvA.png')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


    @commands.command()
    async def avatar(self, ctx, *, user: Union[discord.Member, FetchedUser] = None):
        """Shows a user's enlarged avatar"""
        embed = discord.Embed()
        user = user or ctx.author
        avatar = user.avatar_url_as(static_format='png')
        embed.set_author(name=str(user), url=avatar)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)



    @commands.command(name='gavatar')
    async def guild_avatar(self ,ctx):
        """*Shows the guild icon*"""
        e = discord.Embed(
            title=ctx.guild.name,
            color=ctx.author.color
        )
        e.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Meta(bot))