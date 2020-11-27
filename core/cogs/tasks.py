import json
from datetime import datetime, timedelta
from time import time

from discord import Activity, ActivityType, Embed, Status, HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure, is_owner, group
from data import db


class Tasks(Cog):
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

	@command(name="sts", hidden=True)
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


	@command(name="set_avatar")
	async def change_bot_avatar(self, bot, avatar):
		pass

	@command(name="ping", hidden=True)
	async def ping(self, ctx):
		start = time()
		message = await ctx.send(f"Pong! DWSP latency: {self.bot.latency*1000:,.0f} ms.")
		end = time()

		await message.edit(content=f"Pong! DWSP latency: `{self.bot.latency*1000:,.0f}` ms. Response time: `{(end-start)*1000:,.0f}` ms.")

def setup(bot):
	bot.add_cog(Tasks(bot))