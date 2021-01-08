"""Misc commands"""

import discord
import datetime, time
import sys, platform, psutil
import asyncio
from ..ext.utils import color, emojis as emj
import requests
from data import config
from discord.ext import menus
from typing import Union
from time import strftime
from discord.utils import snowflake_time, cached_property
from discord.ext import commands
from discord import Member, Embed, Color, Status, Guild
from core.ext import utils as u
from ..ext.help import PaginatedHelpCommand

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
    '''Main commands for the bot.'''
    def __init__(self, bot):
        self.old_help_command = bot.help_command
        bot.help_command = PaginatedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(name='fate', aliases=['owner'], hidden=True)
    async def owner_command(self, ctx):
        """Info about the bot maker"""

        embed = discord.Embed(
            title="*Fate's social info*",
            color = color.invis(self),
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


    @commands.command(name="invite", aliases=['join', 'inv'])
    async def _invite(self, ctx):
        """
        Invite this bot
        """
        await ctx.send(
            embed=discord.Embed(
                title="Invite Link",
                description=f"https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}"
                    "&permissions=0&scope=bot",
                colour=color.invis(self),
                )
            )


    @commands.command(name="status")
    async def status_command(self, ctx, *, member: Union[Member, FetchedUser] = None):

        """Display member's status"""
        try:
            member = member or ctx.author
            if member is not None:
                e = discord.Embed(
                    description=f"The member {member.mention}'s status is `{member.status}`",
                    color=color.invis(self)
                )
                await ctx.send(embed=e)
            else:
                member = member or ctx.author
                e = discord.Embed(
                    description=f"Your status is `{member.status}`",
                    color=color.invis(self)
                )
                await ctx.send(embed=e)
                await ctx.send(e)
        except Exception as e:
            await ctx.send(e)


    # this command is yoinked from https://github.com/Rapptz/RoboDanny/ with more stuff added by me



    @commands.command(name="botinfo", aliases=['about', 'bot'])
    async def about(self, ctx: commands.Context):
        """Tells you information about the bot itself."""
        owner_name = f"<@{self.bot._owner}>"
        embed = discord.Embed(
            description=f'Info about [{self.bot.user.name}](https://github.com/nxtlo/Amaya)',
        color=color.invis(self))
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

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
        version = discord.__version__

        embed.add_field(name='<:members:770769874040520734> Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='<:channel:585783907841212418> Channels', value=f'{text + voice} total\n{text} text\n{voice} voice')
        embed.add_field(name='<:ser_emoji:763034584425431110> Guilds', value=guilds)
        embed.add_field(name="<:online:772775766030417962> Uptime", value='{}'.format(self.bot._uptime()))
        embed.add_field(name='<a:processing:770769875051347978> Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')
        embed.add_field(name='<:psql:794233423320711210> Database', value=f'(PostgreSQL) 13.1')
        embed.add_field(name="<:centos:794233424730259456> VM OS", value=f"{os_name}\n" + ' ' + 'CentOS 8')
        embed.add_field(name="<a:loading:393852367751086090> Created at", value=snowflake_time(id=self.bot.user.id).strftime("%A\n%Y/%d/%m\n%H:%M:%S %p"))
        embed.add_field(name="<:dev:763073500155215874> Bot dev", value=owner_name)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f'Made with discord.py v{version}', icon_url='http://i.imgur.com/5BFecvA.png')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


    @commands.command()
    async def avatar(self, ctx, *, user: Union[discord.Member, FetchedUser] = None):
        """Shows a user's enlarged avatar"""
        embed = discord.Embed(color=color.invis(self))
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
            color=color.invis(self)
        )
        e.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=e)

    @commands.command(name="weather")
    async def Weather(self, ctx, *, city: str):
        """
        Show your city's weather

        usage: **weather** `<city_name>`
        """
        api_key = config.weather_api
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel

        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                owner = str(ctx.guild.owner)
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]

                weather_description = z[0]["description"]
                embed = discord.Embed(title=f"Weather in {city_name}",
                                color=ctx.guild.me.top_role.color,
                                timestamp=ctx.message.created_at,)
                embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
                embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
                embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")

                await channel.send(embed=embed)
        else:
            await channel.send("City not found.")


    @commands.command(name="source", aliases=['src'])
    async def _src(self, ctx):
        await ctx.send("https://github.com/nxtlo/Amaya")


    @commands.command(aliases=["serverinfo", 'si'])
    async def sinfo(self, ctx):
        """
        Show server info.
        """
        name = str(ctx.guild.name)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        emoji_count = len(ctx.guild.emojis)
        role_count = len(ctx.guild.roles)
        embed = discord.Embed(
            colour = color.invis(self)
        )

        sOWNER = discord.utils.get(self.bot.emojis, name="owner")
        sID = discord.utils.get(self.bot.emojis, name='rich_presence')
        sREGION = discord.utils.get(self.bot.emojis, name='globe')
        sMEMBERS = discord.utils.get(self.bot.emojis, name='members')
        sEMOJIS = discord.utils.get(self.bot.emojis, name='add_reaction')
        sROLES = discord.utils.get(self.bot.emojis, name='settings')

        boosters = int(ctx.guild.premium_subscription_count)

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.set_author(name=f'{ctx.guild.name}', icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"{sOWNER} **Server Owner**", value=f"{owner}", inline=False)
        embed.add_field(name=f"**<:ser_emoji:763034584425431110> Server ID**", value=f"{id}", inline=True)

        if ctx.guild.premium_tier:
            embed.add_field(name=f"{u.emojis.boost(self)} **Boost tier**", value=ctx.guild.premium_tier, inline=True)
        embed.add_field(name=f"**<a:calen:763440423347290124> Creation date**", value=f"{ctx.guild.created_at}", inline=False)
        embed.add_field(name=f"{sREGION} **Server Region**", value=f"{region}", inline=True)

        if boosters:
            embed.add_field(name=f"{u.emojis.boost(self)} **Boosters**", value=f"{boosters}", inline=True)
        if memberCount:
            embed.add_field(name=f"{sMEMBERS} **Members**", value=f"{memberCount}", inline=False)
        if emoji_count:
            embed.add_field(name=f"**Emojis**", value=f"{emoji_count}", inline=True)
        if role_count:
            embed.add_field(name=f"**Roles**", value=f"{role_count}", inline=True)

        # Get the current guild prefix from the database,
        # We can obviously make it less easier but why bit ¯\_(ツ)_/¯
        current_prefix = await self.bot.pool.fetchval("SELECT prefix FROM prefixes WHERE id = $1", str(ctx.guild.id))

        if current_prefix:
            embed.add_field(name="**Guild Prefix**", value=f"`{current_prefix}`")
        
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @commands.command(name="info", aliases=['ui'])
    async def user_info(self, ctx, *, user: Union[discord.Member, FetchedUser] = None):
        """Show user info"""
        user = user or ctx.author
        e = discord.Embed()
        e.color = color.invis(self)
        roles = [role.mention for role in getattr(user, 'roles', [])]

        mob = user.is_on_mobile()
        custom_stats = user.activity
        booster = user.premium_since

        online = Status.online
        dnd = Status.dnd
        idle = Status.idle
        offline = Status.offline
        
        fmt_time = '%A, %Y/%d/%m, %H:%M:%S %p'

        e.add_field(name=f"{emj.mem(self)} ID", value=user.id, inline=False)
        e.add_field(name=f"{emj.plus(self)} Joined server at", value=user.joined_at.strftime(fmt_time), inline=False)
        e.add_field(name=f"{emj.dscord(self)} Created account",value=user.created_at, inline=False)

        if booster:
            e.add_field(name=f"{emj.boost(self)} Booster since", value=user.premium_since, inline=False)
        if mob:
            e.add_field(name="<:phone:779159717388877846> Is on Mobile", value=mob, inline=False)
        
        if user.top_role:
            e.add_field(name="Top role", value=user.top_role.mention, inline=False)

        if user.status == online:
            e.add_field(name="Status", value=f"{emj.online(self)} {user.status}")

        elif user.status == dnd:
            e.add_field(name="Status", value=f"{emj.dnd(self)} {user.status}")

        elif user.status == idle:
            e.add_field(name="Status", value=f"{emj.idle(self)} {user.status}")

        elif user.status == offline:
            e.add_field(name="Status", value=f"{emj.offline(self)} {user.status}")

        if user.roles:

            e.add_field(name=f'{emj.setting(self)} Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles', inline=False)
        e.set_author(name=str(user))
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)

    @commands.group(name="git")
    async def git(self, ctx):
        """```Useage user: git user <username>```\n```Useage repo: git repo <username> <reponame>```"""
        pass


    @git.command(name="user")
    async def user_command(self, ctx, *, user: str):
        
        try:
            name = user.replace(" ", "+")
            github = "https://github.com/" + name
            await ctx.send(github)
        
        except Exception as e:
            if user is None:
                await ctx.send("Please provide a user" + e)


    @git.command(name="repo")
    async def repo_command(self, ctx, user: str, *, repo: str):
        if user is None:
            await ctx.send("Please provide a user or type `pls git` for more info")
        elif repo is None:
            await ctx.send("Please provide a repo name or type `pls git` for more info")
        
        else:
            repo = repo.replace(" ", "+")
            repo_link = "https://github.com/" + user + "/" + repo
            await ctx.send(repo_link)



def setup(bot):
    bot.add_cog(Meta(bot))
