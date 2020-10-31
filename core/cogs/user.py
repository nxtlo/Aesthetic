import discord
from discord.ext import commands
from data import db
import datetime
from typing import Union
from core.cogs.commands import FetchedUser
from core.ext.utils import emojis as emj

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="register", aliases=['reg'], discription='Register to the database')
    @commands.guild_only()
    async def register_command(self, ctx):
        """*Register to the database*"""
        db.cur.execute("SELECT * FROM users WHERE id=?", (ctx.author.id,))
        
        response = db.cur.fetchone()
        
        if response:
            embed = discord.Embed(
                title=":grey_exclamation: You're already in the database. type `??help` for more info",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=embed)
        else:
            db.cur.execute("INSERT INTO users VALUES (?,?,?,?)",
                (ctx.author.id, 
                ctx.author.name,
                ctx.author.discriminator,
                ctx.author.joined_at))
            db.con.commit()
            try:
                await ctx.message.add_reaction("âœ…")
                print(str(ctx.author.name) + "was added to the database")
            except Exception as e:
                raise e
    

    @commands.command(name="info")
    async def user_info(self, ctx, *, user: Union[discord.Member, FetchedUser] = None):
        """Show user info"""
        user = user or ctx.author
        e = discord.Embed()
        e.color = ctx.author.color
        roles = [role.name.replace('@', '@\u200b') for role in getattr(user, 'roles', [])]
        
        mob = user.is_on_mobile()


        e.add_field(name=f"{emj.mem(self)} ID", value=user.id)
        e.add_field(name=f"{emj.plus(self)} Joined server at", value=user.joined_at)
        e.add_field(name=f"{emj.dscord(self)} Created account",value=user.created_at)
        e.add_field(name=f"{emj.boost(self)} Booster since", value=user.premium_since)
        if mob:
            e.add_field(name=":mobile_phone: Is on Mobile", value=mob)
        e.add_field(name="Custom Status", value=user.activity)
        e.add_field(name="Status", value=user.status)
        e.add_field(name=f'{emj.setting(self)} Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles', inline=False)
        e.set_author(name=str(user))
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)

        """
        @commands.Cog.listener()
        async def on_message(self, message, member: discord.Member):
            if "??reg" in message.content:
                role = u.role.verified(self)
                if message.author not in role:
                    await message.delete()
                    await member.add_role(role)
                    """

def setup(bot):
    bot.add_cog(User(bot))