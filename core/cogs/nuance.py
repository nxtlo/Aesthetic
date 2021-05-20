import discord
from discord.ext import commands
from ..ext import check

NUANCE_GUILD_ID = 764317052068298772
AMAYA_GUILD_ID = 411804307302776833

class Nuance(commands.Cog):
    '''Exclusive commands for the clan.'''
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='autorole', hidden=True)
    async def set_role(self, ctx, role: discord.Role):
        role = role.id or role.mention
        if (ctx.guild.id == NUANCE_GUILD_ID or ctx.guild.id == AMAYA_GUILD_ID):
            await ctx.pool.execute("INSERT INTO nuance(id, role_id) VALUES($1, $2)", ctx.guild.id, role.id)
            await ctx.send(f"Autorole has been set to {role.mention}.")
        else:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if (member.guild.id == NUANCE_GUILD_ID or member.guild.id == AMAYA_GUILD_ID):
            if member.bot:
                return
            roleid = await self.bot.pool.fetchrow("SELECT role_id FROM nuance")
            if roleid is None:
                pass
            toadd = discord.Object(id=roleid['role_id'])
            if toadd not in member.roles:
                await member.add_roles(toadd)
            else:
                return

def setup(bot):
    bot.add_cog(Nuance(bot))