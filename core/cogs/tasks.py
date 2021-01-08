import json
from datetime import datetime, timedelta
from time import time
from discord import Activity, ActivityType, Embed, Status, HTTPException, TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure, is_owner, group
from typing import Optional
from ..ext import check
from discord import Color
from ..ext.utils import color

class Utility(Cog, name='\U00002699 Utility'):
	'''Commands for config the bot.'''
	def __init__(self, bot):
		self.bot = bot



	@command(name='ping')
	async def _ping(self, ctx):
		await ctx.message.add_reaction('\U00002705')


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