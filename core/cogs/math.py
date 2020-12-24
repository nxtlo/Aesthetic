from discord.ext.commands import command, Cog, group
from discord import Embed
from decimal import Decimal
from ..ext.converters import convert
from ..ext.utils import color



class Math(Cog, name="\U0001f9ee Math"):
    def __init__(self, bot):
        self.bot = bot

    @command(name="calc")
    async def calculator(self, ctx, int1: int, opp: str, int2: int):
        """**Available Operations:**\n `+`: **Sum two numbers.**\n `-`: **Remove a numbers**\n `*`: **Multiply numbers**\n `%`: **Modulo division**\n `/`: **Divides two numbers**"""
        try:
            if opp == '+':
                e = Embed(title=f"{int1 + int2}", color=color.invis(self))
                await ctx.send(embed=e)
            elif opp == '-':
                e = Embed(title=f"{int1 - int2}", color=color.invis(self))
                await ctx.send(embed=e)
            elif opp == '*':
                e = Embed(title=f"{int1 * int2}", color=color.invis(self))
                await ctx.send(embed=e)
            elif opp == '%':
                e = Embed(title=f"{int1 % int2}",color=color.invis(self))
                await ctx.send(embed=e)
            elif opp == '/':
                e = Embed(title=f"{int1 / int2}", color=color.invis(self))
                await ctx.send(embed=e)
            else:
                await ctx.send(f"Couldn't calculate {int1} and {int2}")
        except Exception as err:
            await ctx.send(err)


    @command(name="bin")
    async def bin(self, ctx, num):
        """Converts a binary number to a decimal"""
        try:
            good = convert.to_bin(self, bnum=num)

            e = Embed(
                title=good,
                color=color.invis(self)
            )
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(e)
            

    @command(name="dec")
    async def decimal(self, ctx, num: int):
        """Converts a decimal number to binary"""
        full = "{0:b}".format(num)
        e = Embed(
            title=full,
            color=color.invis(self)
        )
        await ctx.send(embed=e)


    @command(name="text")
    async def _text(self, ctx, text):
        """Converts text to binary"""
        e = Embed(
            title=convert.to_text(self, text=text),
            color=color.invis(self)
        )
        await ctx.send(embed=e)



def setup(bot):
    bot.add_cog(Math(bot))