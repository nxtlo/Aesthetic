import aiobungie
from data import config
from discord.ext.commands import command, group, Cog
from discord import Embed
from httpx import AsyncClient

PREVAIL_CLAN = 4389205
class Destiny(Cog, name="<:Destiny2:666084830987026443> Destiny"):
    """Destiny 2 stuff."""
    _client = aiobungie.Client(config.bungie_key)
    def __int__(self, bot):
        self.bot = bot


    @group(aliases=['d2'])
    async def destiny(self, ctx):
        pass

    @destiny.command(name='clan')
    async def _clan(self, ctx, clan: int = None):
        clan = clan or PREVAIL_CLAN
        result = await self._client.get_clan(clan)
        e = Embed(title=f"{result.name} - {result.id}", description=result.description)
        e.set_author(name=result.about)
        #e.set_thumbnail(url=result.avatar)
        e.set_image(url=result.banner)
        e.set_thumbnail(url=result.avatar)
        e.add_field(name='Owner', value=result.owner)
        e.add_field(name='Members', value=result.member_count)
        e.add_field(name='Is Public', value=result.is_public)
        e.add_field(name='Edited at', value=result.edited_at)
        e.set_footer(text=f"Created at {result.created_at}")
        try:
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(e)

    @destiny.command(name='api')
    async def _user(self, ctx, app = None):
        app = app or 38349
        g = await self._client.get_app(app)
        e = Embed(description=f"[{g.name}]({g.redirect_url})")
        e.set_author(name=g.id, icon_url=BUNGIE_URL + g.icon_path)
        e.add_field(name="App Owner", value=f"[{g.owner_name}]({BUNGIE_URL}en/Profile/{g.owner_id})", inline=False)
        e.add_field(name="Created at", value=g.created_at, inline=False)
        e.add_field(name="Status", value=g.status, inline=False)
        e.add_field(name="Public App?", value=g.is_public)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Destiny(bot))
