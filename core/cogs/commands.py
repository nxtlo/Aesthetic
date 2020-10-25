import discord
from discord.ext import commands
from discord import utils as us
from core.ext import utils as u
import datetime, time
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
        if 'hi' in message.content:
            try:
                await message.channel.send("sup :sunglasses:")
            except:
                pass


def setup(bot):
    bot.add_cog(Commands(bot))