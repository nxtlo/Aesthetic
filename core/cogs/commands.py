import discord
import sqlite3
import datetime, time

from discord.ext import commands
from discord import utils as us
from core.ext import utils as u


    ### Red-bot api for botstats command and listguilds

from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, close_menu
from redbot.core.utils.common_filters import filter_invites
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import chat_formatting as cf

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='fate', aliases=['socials'] ,discription="Fate's social media stuff")
    async def owner_command(self, ctx):

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


    @commands.command(name='restart' ,discription="Restart command", hidden=True)
    @commands.is_owner()
    async def restart_command(self, ctx):
        try:
            embed = discord.Embed(
                title=f"{ctx.author} ***Restarting now...!***",
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)
            await self.bot.logout()
        except:
            raise
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("hi"):
            try:
                await message.channel.send("sup :sunglasses:")
            except:
                pass
    


    # commands under are not mine -> Trusty-cogs / aikaterna-cogs / redbot-core

    @commands.command()
    async def botstats(self, ctx: commands.Context) -> None:
        _ = Translator("ServerStats", __file__)
        """Display stats about the bot"""
        async with ctx.typing():
            servers = len(ctx.bot.guilds)
            passed = (datetime.datetime.utcnow() - ctx.me.created_at).days
            since = ctx.me.created_at.strftime("%d %b %Y %H:%M")
            msg = _(
                "{bot} is on {servers} servers serving {members} members!\n"
                "{bot} was created on **{since}**.\n"
                "That's over **{passed}** days ago!"
            ).format(
                bot=ctx.me.mention,
                servers=servers,
                members=len(self.bot.users),
                since=since,
                passed=passed,
            )
            em = discord.Embed(
                description=msg, colour=ctx.author.color, timestamp=ctx.message.created_at
            )
            if ctx.guild:
                em.set_author(
                    name=f"{ctx.me} {f'~ {ctx.me.nick}' if ctx.me.nick else ''}",
                    icon_url=ctx.me.avatar_url,
                )
            else:
                em.set_author(
                    name=f"{ctx.me}",
                    icon_url=ctx.me.avatar_url,
                )
            em.set_thumbnail(url=ctx.me.avatar_url)
            if ctx.channel.permissions_for(ctx.me).embed_links:
                await ctx.send(embed=em)
            else:
                await ctx.send(msg)


    @commands.command(name="listguilds", aliases=["listservers", "guildlist", "serverlist"], hidden=True)
    @commands.is_owner()
    async def listguilds(self, ctx):
        """servers the bot is in."""
        asciidoc = lambda m: "```asciidoc\n{}\n```".format(m)
        guilds = sorted(self.bot.guilds, key=lambda g: -g.member_count)
        header = ("```\n" "The bot is in the following {} server{}:\n" "```").format(
            len(guilds), "s" if len(guilds) > 1 else ""
        )

        max_zpadding = max([len(str(g.member_count)) for g in guilds])
        form = "{gid} :: {mems:0{zpadding}} :: {name}"
        all_forms = [
            form.format(
                gid=g.id,
                mems=g.member_count,
                name=filter_invites(cf.escape(g.name)),
                zpadding=max_zpadding
            )
            for g in guilds
        ]
        final = "\n".join(all_forms)

        await ctx.send(header)
        page_list = []
        for page in cf.pagify(final, delims=["\n"], page_length=1000):
            page_list.append(asciidoc(page))

        if len(page_list) == 1:
            return await ctx.send(asciidoc(page))
        await menu(ctx, page_list, DEFAULT_CONTROLS)

def setup(bot):
    bot.add_cog(Commands(bot))