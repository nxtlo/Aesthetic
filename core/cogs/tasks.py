from discord import Embed, Status, Member
from discord.ext import menus
from discord.ext.commands import command, is_owner, group, Cog
from typing import Optional
from ..ext import check, pagination
from ..ext.utils import color as c
from corona_python import Country, World
from sr_api import image, Client as _client
import time
import colour

class Utility(Cog, name='\U00002699 Utility'):
	'''Commands for config the bot and other Utils.'''
	def __init__(self, bot):
		self.bot = bot
		self._country = Country
		self._world = World()



	@command(name="filter")
	async def _filter(self, ctx, option = None, image = None):
		"""Filter an image, type filters for more info about the filters."""
		try:
			resp = _client().filter(url=image, option=option)
			e = Embed(color=c.invis(self))
			e.set_image(url=resp)
			await ctx.send(embed=e)
		except Exception as e:
			await ctx.send(e)

	@command(name="filters")
	async def show_filters(self, ctx):
		options = (
			'greyscale', 'invert', 'invertgreyscale', 'brightness', 'threshold', 'sepia', 'red', 'green', 'blue', 'blurple',
			'pixelate', 'blur', 'gay', 'glass', 'wasted', 'triggered', 'spin')
		p = pagination.SimplePages(entries=options)
		await p.start(ctx)

	@group(name='color', invoke_without_command=True)
	async def color_cmd(self, ctx, *, color = None):
		'''
		Returns a human readble color by its name.

		Examples: 
		```color blue```
		```color red```
		```color violet```
		```color indigo```
		'''
		cl = _client()
		e = Embed(title=colour.Color(color).hex ,color=c.invis(self))
		e.set_image(url=cl.view_color(colour.Color(color).hex))
		try:
			await ctx.send(embed=e)
		except ValueError:
			pass



	@color_cmd.command()
	async def list(self, ctx):
		"""Shows all available colors."""
		colors = colour.COLOR_NAME_TO_RGB
		p = pagination.SimplePages(entries=[c for c in [*colors]], per_page=10)
		p.embed.color = c.random(self)
		try:
			await p.start(ctx)
		except menus.MenuError as e:
			await ctx.send(e)

	@command()
	async def covid(self, ctx, *, country: Optional[str]=None):
		if country is not None:
			e = Embed(title=f"Covid stats for {country}", color=c.invis(self))
			country = self._country(country)
			if country.flag():
				e.set_image(url=country.flag())
			e.add_field(name='\U0000274c Active cases', value=country.active())
			e.add_field(name="\U0000274c Today's cases", value=country.today_cases())
			e.add_field(name='\U0000274c Total cases', value=country.total_cases())
			e.add_field(name="\U0000274c Today's deaths", value=country.today_deaths())
			e.add_field(name='\U0000274c Total deaths', value=country.total_deaths())
			e.add_field(name='\U0000274c Total criticals', value=country.critical())
			e.add_field(name='\U00002705 Total recovered', value=country.recovered())
			e.add_field(name='\U0001f30e Continent', value=country.continent())
			e.add_field(name="\U00002705 Today's recovered", value=country.today_recovered())
			await ctx.send(embed=e)
		else:
			e = Embed(title=f"Covid stats for the world. \U0001f30e", color=c.invis(self))
			e.add_field(name='\U0000274c Active cases', value=self._world.active_cases())
			e.add_field(name="\U0000274c Today's cases", value=self._world.today_cases())
			e.add_field(name='\U0000274c Total cases', value=self._world.total_cases())
			e.add_field(name='\U0000274c Last Updated', value=self._world.last_updated())
			e.add_field(name="\U0000274c Today's deaths", value=self._world.today_deaths())
			e.add_field(name='\U0000274c Total deaths', value=self._world.total_deaths())
			e.add_field(name='\U0000274c Total criticals', value=self._world.critical_cases())
			e.add_field(name='\U00002705 Total recovered', value=self._world.recovered())
			e.add_field(name="\U00002705 Today's recovered", value=self._world.today_recovered())
			e.set_footer(text=f"World Population {self._world.population()}")
			await ctx.send(embed=e)


	@command(name='ping')
	async def _ping(self, ctx):
		before = time.time()
		e = Embed(title='Pong! \U0001f3d3', description=f"API Latency: {int(round(self.bot.latency * 1000))}\nMessage Latency: {before - time.time()}")
		await ctx.send(embed=e)


	@group(name="set")
	async def setter(self, ctx):
		pass


	@setter.command(name="prefix")
	@check.is_mod()
	async def change_prefix(self, ctx, prefix: Optional[str]):
		"""
		Change the bot's prefix. 
		You need the manage_guild perms to use this command.
		"""
		if len(prefix) > 6:
			await ctx.send("Prefix too long.")
			
		query = "SELECT prefix FROM prefixes WHERE id = $1"
		method = await self.bot.pool.fetchval(query, ctx.guild.id)

		if not method:
			await self.bot.pool.execute("INSERT INTO prefixes(id, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
			await ctx.send(f"Prefix changed to {prefix}")
		else:
			query = "UPDATE prefixes SET prefix = $1 WHERE id = $2"
			await self.bot.pool.execute(query, prefix, ctx.guild.id)
			await ctx.send(f"Prefix updated to {prefix}")


	@setter.command(name="sts", hidden=True)
	@is_owner()
	async def change_sts(self, ctx, stts: str):
		try:
			discord_status = ["dnd", "offline", "idle", "online"]
			
			if stts not in discord_status:
				await ctx.send(f"Couldn't change the status to `{stts}`")
			else:
				if stts == "dnd":
					await self.bot.change_presence(status=Status.dnd)
					await ctx.send(f"Status changed to `{stts}`")
				elif stts == "idle":
					await self.bot.change_presence(status=Status.idle)
					await ctx.send(f"Status changed to `{stts}`")
				elif stts == "offline":
					await self.bot.change_presence(status=Status.offline)
					await ctx.send(f"Status changed to `{stts}`")
				elif stts == "online":
					await self.bot.change_presence(status=Status.online)
					await ctx.send(f"Status changed to `{stts}`")
		except:
			raise

def setup(bot):
	bot.add_cog(Utility(bot))
