import discord
from discord.ext import commands
import sys
import asyncio

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='owner', aliases=['socials'] ,discription="Fate's social media stuff")
    async def owner_command(self, ctx):

        embed = discord.Embed(
            title="*Fate's social info*",
            color = ctx.author.color,
            timestamp =ctx.message.created_at,
        )
        d = discord.utils.get

        insta = d(self.bot.emojis, name='insta')
        twitter = d(self.bot.emojis, name='twitter')
        utube = d(self.bot.emojis, name='youtube')
        steam = d(self.bot.emojis, name='steam')
        github = d(self.bot.emojis, name='github')
        bungie = d(self.bot.emojis, name='bungie')

        embed.add_field(name=f"{insta} ```Instagram```", value="[Click Here](https://instagram.com/nxtlo)", inline=True)
        embed.add_field(name=f"{twitter} ```Twitter```", value="[Click Here](https://twitter.com/helfate)", inline=True)
        embed.add_field(name=f"{utube} ```Youtube```", value="[Click Here](https://youtube.com/channel/UC4acY39W-lBjgiqOBsaoqJw)", inline=True)
        embed.add_field(name=f"{steam} ```Steam```", value="[Click Here](https://steamcommunity.com/id/LordhaveFate/)", inline=True)
        embed.add_field(name=f"{github} ```Github```", value="[Click Here](https://github.com/nxtlo)", inline=True)
        embed.add_field(name=f"{bungie} ```Bungie```", value="[Click Here](https://www.bungie.net/en/Profile/254/20315338/Fate)")
        embed.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
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

def setup(bot):
    bot.add_cog(Commands(bot))