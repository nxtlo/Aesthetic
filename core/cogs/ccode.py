from cxcode import proto
from discord.ext.commands import command, Cog, Context, Command

class CCode(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='csum')
    async def csum(self, ctx, x: int, y: int) -> float:
        await ctx.send(proto.from_sqrt(x, y))

    @command(name='node')
    async def node(self, ctx, target: int) -> int:
        func = proto.fromNode([1,2,3,4,32,6,1], target)
        await ctx.send(func)

    @command(name='member')
    async def member(self, ctx):
        await ctx.send(proto.get())


def setup(bot):
    bot.add_cog(CCode(bot))