from discord.ext.commands import command, Cog, is_nsfw, NSFWChannelRequired
from discord import Embed
import scathach
from ..ext.utils import color

class Hentai(Cog):
    '''NSFW commands.'''
    def __init__(self, bot):
        self.bot = bot


    @command(name="bikini")
    @is_nsfw()
    async def _bikini(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.bikini())
        await ctx.send(embed=e)


    @command(name='ass')
    @is_nsfw()
    async def _ass(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.ass())
        await ctx.send(embed=e)

    @command(name='pussy')
    @is_nsfw()
    async def _pussy(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.pussy_juice())
        await ctx.send(embed=e)

    @command(name='blush')
    @is_nsfw()
    async def _blush(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.blush())
        await ctx.send(embed=e)

    @command(name='gif')
    @is_nsfw()
    async def _gif(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.gif())
        await ctx.send(embed=e)

    @command(name='thick')
    @is_nsfw()
    async def _thick(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.thick())
        await ctx.send(embed=e)


    @command(name='yuri')
    @is_nsfw()
    async def _yuri(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.yuri())
        await ctx.send(embed=e)

    @command(name='perv')
    @is_nsfw()
    async def _perv(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.pervert())
        await ctx.send(embed=e)


    @command(name='himiko')
    @is_nsfw()
    async def _himiko(self, ctx):
        e = Embed(color=color.invis(self))
        e.set_image(url=scathach.himiko())
        await ctx.send(embed=e)

    @Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, NSFWChannelRequired):
            await ctx.send("This command can only be used in an NSFW channel.")


def setup(bot):
    bot.add_cog(Hentai(bot))