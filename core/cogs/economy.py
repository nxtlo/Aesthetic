import discord
from discord.ext import commands
import datetime,time


# <---- Soon :) ----> #

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.group(name="doz")
    async def doz(self, ctx):
        """
        Currency name is DOZ
        """
        pass


    @doz.command(name="balance", aliases=['bal', 'bank'])
    async def balance_command(self, ctx, member: discord.Member):
        pass


    @doz.command(name="add")
    async def add_command(self, ctx, member: discord.Member):
        pass



def setup(bot):
    bot.add_cog(economy(bot))