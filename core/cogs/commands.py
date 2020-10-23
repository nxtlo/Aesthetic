import discord

from discord.ext import commands
from discord import utils as us
from ext import utils as u

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='owner', aliases=['socials'] ,discription="Fate's social media stuff")
    async def owner_command(self, ctx):
        
        insta = us.get(self.bot.emojis, name="insta")
        twitter = us.get(self.bot.emojis, name="twitter")
        bungie = us.get(self.bot.emojis, name="bungie")
        steam = us.get(self.bot.emojis, name="steam")
        github = us.get(self.bot.emojis, name="github")
        utube = us.get(self.bot.emojis, name="youtube")

        embed = discord.Embed(
            title="*Fate's social info*",
            color = ctx.author.color,
            timestamp =ctx.message.created_at,
        )
        embed.add_field(name=f"{insta} ```Instagram```", value=u.url.insta, inline=True)
        embed.add_field(name=f"{twitter} ```Twitter```", value=u.url.twitter, inline=True)
        embed.add_field(name=f"{utube} ```Youtube```", value=u.url.youtube, inline=True)
        embed.add_field(name=f"{steam} ```Steam```", value=u.url.steam, inline=True)
        embed.add_field(name=f"{github} ```Github```", value=u.url.github, inline=True)
        embed.add_field(name=f"{bungie} ```Bungie```", value=u.url.bungie)
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