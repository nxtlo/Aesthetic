import json
from datetime import datetime, timedelta
from time import time
from discord import Activity, ActivityType, Embed, Status, HTTPException, TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure, is_owner, group
from ..ext import check
from discord import Color
from ..ext.utils import color

class Utility(Cog, name='\U00002699 Utility'):
	def __init__(self, bot):
		self.bot = bot


	@group(name="set")
	async def setter(self, ctx):
		pass


	@setter.command(name="prefix")
	@check.is_mod()
	async def change_prefix(self, ctx, prefix):
		"""
		Change the bot's prefix. 
		You need the manage_guild perms to use this command.
		"""
		try:
			if len(prefix) > 5:
				await ctx.send("Prefix cannot be longer the 5")
			get = await self.bot.pool.tables['prefixes'].select(
				'prefix',
				where={
					'id': ctx.guild.id
				}
			)
			if not get:
				await self.bot.pool.tables['prefixes'].insert(
					prefix=prefix,
					id=ctx.guild.id
				)
				e = Embed(description=f"prefix changed to `{prefix}`")
				await ctx.send(embed=e)
			else:
				await self.bot.pool.tables['prefixes'].update(
						prefix=prefix,
						where={
							'id': ctx.guild.id
						}
					)
				await ctx.send(f"Updated prefix to {prefix}")
		except Exception as e:
			await ctx.send(e)

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