import json
from datetime import datetime, timedelta
from time import time
from discord import Activity, ActivityType, Embed, Status, HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure, is_owner, group
from data import db
from discord import Color
from ..ext.utils import color

<<<<<<< HEAD

class Tasks(Cog):
=======
class Tasks(Cog, name='\U00002699 Tasks'):
>>>>>>> ab319af95de7c20e10659af729e11a8048f5768c
	def __init__(self, bot):
		self.bot = bot

	@property
	def message(self):
		return self._message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

	@message.setter
	def message(self, value):
		if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
			raise ValueError("Invalid activity type.")

		self._message = value

	async def set(self):
		_type, _name = self.message.split(" ", maxsplit=1)

		await self.bot.change_presence(activity=Activity(
			name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
		))
	
	@command(name="activity", aliases=['act'], hidden=True)
	@is_owner()
	async def set_activity_message(self, ctx, *, text: str):
		self.message = text
		await self.set()

	@group(name="set")
	async def setter(self, ctx):
		"""Command to set the main Config for the bot"""
		pass
	
	@setter.command(name="help")
	async def set_command(self, ctx):
		stuff = """
				set prefix `<prefix>`
				set stts `<status>` -> `idle` / `dnd` / `offline` / `online`
				set avatar `<url>`
				set username `<name>`
				set <nickname> `<name>`
				"""
		e = Embed(
			color=ctx.author.color,
			title="Commands avilable for `set`",
			description=stuff
		)
		await ctx.send(embed=e)
			

	@setter.command(name="prefix")
	@has_permissions(administrator=True)
	async def change_prefix(self, ctx, prefix):
		"""
		Change the bot's prefix
		"""
		try:
			if len(prefix) > 5:
				await ctx.send("The prefix can not be more than 5 characters in length.")

			else:
				db.execute("UPDATE Guilds SET prefix = ? WHERE id = ?", prefix, ctx.guild.id)
				db.con.commit()
				e = Embed(description=f"{ctx.author.mention} has changed the prefix to `{prefix}`")
				await ctx.send(embed=e)
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


	@command(name="ar")
	async def ar_info(self, ctx):
		pass


def setup(bot):
	bot.add_cog(Tasks(bot))