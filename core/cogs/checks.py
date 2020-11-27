import discord
import random

from discord.ext import commands
from core.ext import check



class checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="This command is missing an Argument.",
                colour = random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=embed)
        

        elif isinstance(err, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="I don't have permissions to do that.",
                colour = random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=embed)

        elif isinstance(err, commands.CommandNotFound):
            return

        elif isinstance(err, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="This command is on cooldown.",
                colour = random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=embed)

        elif isinstance(err, commands.NotOwner):
            embed = discord.Embed(
                title="Only owner can use this command.",
                colour = random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=embed)
        else:
            raise err


def setup(bot):
    bot.add_cog(checks(bot))