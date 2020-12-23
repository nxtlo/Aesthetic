"""Misc commands"""

import discord
import datetime, time
import sys, platform, psutil
import asyncio
from ..ext.pagination import Pages
from ..ext.utils import color, emojis as emj
import requests
from data import config
from discord.ext import menus
from typing import Union
from discord.ext import commands
from discord import Member, Embed, Color, Status, Guild
from data import db
from core.ext import utils as u
start_time = time.time()


# yes the help command is frm R.Danny

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


class BotHelpPageSource(menus.ListPageSource):
    def __init__(self, help_command, commands):
        # entries = [(cog, len(sub)) for cog, sub in commands.items()]
        # entries.sort(key=lambda t: (t[0].qualified_name, t[1]), reverse=True)
        super().__init__(entries=sorted(commands.keys(), key=lambda c: c.qualified_name), per_page=6)
        self.commands = commands
        self.help_command = help_command
        self.prefix = help_command.clean_prefix

    def format_commands(self, cog, commands):
        # A field can only have 1024 characters so we need to paginate a bit
        # just in case it doesn't fit perfectly
        # However, we have 6 per page so I'll try cutting it off at around 800 instead
        # Since there's a 6000 character limit overall in the embed
        if cog.description:
            short_doc = cog.description.split('\n', 1)[0] + '\n'
        else:
            short_doc = '\u0020'

        current_count = len(short_doc)
        ending_note = '+%d not shown'
        ending_length = len(ending_note)

        page = []
        for command in commands:
            value = f'`{command.name}`'
            count = len(value) + 1 # The space
            if count + current_count < 800:
                current_count += count
                page.append(value)
            else:
                # If we're maxed out then see if we can add the ending note
                if current_count + ending_length + 1 > 800:
                    # If we are, pop out the last element to make room
                    page.pop()

                # Done paginating so just exit
                break

        if len(page) == len(commands):
            # We're not hiding anything so just return it as-is
            return short_doc + ' '.join(page)

        hidden = len(commands) - len(page)
        return short_doc + ' '.join(page) + '\n' + (ending_note % hidden)


    async def format_page(self, menu, cogs):
        prefix = menu.ctx.prefix
        description = f'Use "{prefix}help command" for more info on a command.'

        embed = discord.Embed(title=f'Commands available', description=description, colour=color.invis(self))

        for cog in cogs:
            commands = self.commands.get(cog)
            if commands:
                value = self.format_commands(cog, commands)
                embed.add_field(name=cog.qualified_name, value=value, inline=True)

        maximum = self.get_max_pages()
        embed.set_footer(text=f'Page {menu.current_page + 1}/{maximum}')
        return embed

class GroupHelpPageSource(menus.ListPageSource):
    def __init__(self, group, commands, *, prefix):
        super().__init__(entries=commands, per_page=6)
        self.group = group
        self.prefix = prefix
        self.title = f'{self.group.qualified_name} Commands'
        self.description = self.group.description

    async def format_page(self, menu, commands):
        embed = discord.Embed(title=self.title, description=self.description, colour=color.invis(self))

        for command in commands:
            signature = f'{command.qualified_name} {command.signature}'
            embed.add_field(name=signature, value=command.short_doc or 'No help given...', inline=False)

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(name=f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} commands)')

        embed.set_footer(text=f'Use "{self.prefix}help command" for more info on a command.')
        return embed

class HelpMenu(Pages):
    def __init__(self, source):
        super().__init__(source)

    @menus.button('\N{WHITE QUESTION MARK ORNAMENT}', position=menus.Last(5))
    async def show_bot_help(self, payload):
        """shows how to use the bot"""

        embed = discord.Embed(title='Using the bot', colour=color.invis(self))
        embed.title = 'Using the bot'
        embed.description = 'Hello! Welcome to the help page.'

        entries = (
            ('<argument>', 'This means the argument is __**required**__.'),
            ('[argument]', 'This means the argument is __**optional**__.'),
            ('[A|B]', 'This means that it can be __**either A or B**__.'),
            ('[argument...]', 'This means you can have multiple arguments.\n' \
                              'Now that you know the basics, it should be noted that...\n' \
                              '__**You do not type in the brackets!**__')
        )

        embed.add_field(name='How do I use this bot?', value='Reading the bot signature is pretty simple.')

        for name, value in entries:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=f'We were on page {self.current_page + 1} before this message.')
        await self.message.edit(embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_page(self.current_page)

        self.bot.loop.create_task(go_back_to_current_page())

class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category'
        })

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True)

        all_commands = {}
        for command in entries:
            if command.cog is None:
                continue
            try:
                all_commands[command.cog].append(command)
            except KeyError:
                all_commands[command.cog] = [command]


        menu = HelpMenu(BotHelpPageSource(self, all_commands))

        await menu.start(self.context)

    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        menu = HelpMenu(GroupHelpPageSource(cog, entries, prefix=self.clean_prefix))

        await menu.start(self.context)

    def common_command_formatting(self, embed_like, command):
        embed_like.title = self.get_command_signature(command)
        if command.description:
            embed_like.description = f'{command.description}\n\n{command.help}'
        else:
            embed_like.description = command.help or None

    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=color.invis(self))
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        if len(entries) == 0:
            return await self.send_command_help(group)

        source = GroupHelpPageSource(group, entries, prefix=self.clean_prefix)
        self.common_command_formatting(source, group)
        menu = HelpMenu(source)
        await menu.start(self.context)


class Meta(commands.Cog, name="\U0001f587 Meta"):
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



    @commands.command(name="botinfo")
    async def about(self, ctx: commands.Context):
        """Tells you information about the bot itself."""
        owner_name = f"<@{self.bot._owner}>"
        embed = discord.Embed(
        color=color.invis(self))
        embed.title=f'Info about {self.bot.user.name}'

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
        version = discord.__version__

        embed.add_field(name='Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='Channels', value=f'{text + voice} total\n{text} text\n{voice} voice')
        embed.add_field(name='Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='Guilds', value=guilds)
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')
        embed.add_field(name="VM OS", value=os_name + os_release)
        embed.add_field(name="Bot owner", value=owner_name)
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

    @commands.command("prefx")
    async def _pfx(self, ctx):
        def inner():
            pfx = db.cur.execute("SELECT prefix FROM Guilds WHERE id = ?", (ctx.guild.id,))
            for prefix in pfx.fetchone():
                return prefix
        e = Embed(
            title="Prefix is:",
            description=f"1: **{inner()}**",
            color=color.invis(self)
            )
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


    @commands.command(aliases=["serverinfo"])
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


        embed.set_author(name=f'Server info for {ctx.guild.name}', icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"{sOWNER} **Server Owner**", value=f"{owner}", inline=False)
        embed.add_field(name=f"**<:ser_emoji:763034584425431110> Server ID**", value=f"{id}", inline=False)
        embed.add_field(name=f"**<a:calen:763440423347290124> Creation date**", value=f"{ctx.guild.created_at}", inline=False)
        embed.add_field(name=f"{sREGION} **Server Region**", value=f"{region}", inline=False)
        if boosters:
            embed.add_field(name=f"{u.emojis.boost(self)} **Boosters**", value=f"{boosters}", inline=False)
        if memberCount:
            embed.add_field(name=f"{sMEMBERS} **Members**", value=f"{memberCount}", inline=False)
        if emoji_count:
            embed.add_field(name=f"**Emojis**", value=f"{emoji_count}", inline=False)
        if role_count:
            embed.add_field(name=f"**Roles**", value=f"{role_count}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @commands.command(name="info")
    async def user_info(self, ctx, *, user: Union[discord.Member, FetchedUser] = None):
        """Show user info"""
        user = user or ctx.author
        e = discord.Embed()
        e.color = color.invis(self)
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
    bot.add_cog(Meta(bot))
