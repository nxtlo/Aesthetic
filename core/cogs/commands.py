import discord
from discord.ext import commands
import sys
import asyncio
from ext import socials as sc

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

        insta = sc.emj(self.bot.emojis, name='insta')
        twitter = sc.emj(self.bot.emojis, name='twitter')
        utube = sc.emj(self.bot.emojis, name='youtube')
        steam = sc.emj(self.bot.emojis, name='steam')
        github = sc.emj(self.bot.emojis, name='github')
        bungie = sc.emj(self.bot.emojis, name="bungie")

        embed.add_field(name=f"{insta} ```Instagram```", value=sc.insta, inline=True)
        embed.add_field(name=f"{twitter} ```Twitter```", value=sc.twitter, inline=True)
        embed.add_field(name=f"{utube} ```Youtube```", value=sc.youtube, inline=True)
        embed.add_field(name=f"{steam} ```Steam```", value=sc.steam, inline=True)
        embed.add_field(name=f"{github} ```Github```", value=sc.github, inline=True)
        embed.add_field(name=f"{bungie} ```Bungie```", value=sc.bungie)
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

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if 'hi' in message.content:
            try:
                await message.channel.send("sup :sunglasses:")
            except:
                pass
def setup(bot):
    bot.add_cog(Commands(bot))