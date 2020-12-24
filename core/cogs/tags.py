from discord.ext.commands import command, Cog, group, Context
from discord import Embed, Member, Color
from typing import Optional

class Tags(Cog, name="\U0001f4cc Tags"):
    def __init__(self, bot):
        self.bot = bot


    @group(invoke_without_command=True)
    async def tag(self, ctx, *, name):
        try:
            tag = await self.bot.pool.tables['tags'].select(
            'content',
            where={
                'guild_id': ctx.guild.id,
                'tag_name': name
            }
        )   
            if not tag:
                await ctx.send("Tag not found.")
                
            if tag:
                for t in tag:
                    t = "".join((str(t).replace("{","").replace("}", "").replace("'content': ", "").replace("'", "").replace("'", ""))).strip('\n')
                await ctx.send(f"{t}")
        except Exception as e:
            await ctx.send(e)
        

    @tag.command()
    async def add(self, ctx, name, *, content):
        
        if name and content is not None:
            await self.bot.pool.tables['tags'].insert(
                guild_id=ctx.guild.id,
                tag_name=name,
                tag_owner=ctx.author.id,
                content=content
            )
            await ctx.send(f"Created tag `{name}`")
        else:
            await ctx.send("Something is missing.")

    
    @tag.command(name='remove', aliases=['del', 'rem'])
    async def rem_tag(self, ctx, *, name):
        
        check = await self.bot.pool.tables['tags'].select(
            'tag_owner',
            where={
                'tag_owner': ctx.author.id,
                'guild_id': ctx.guild.id
            }
        )
        if check:
            await self.bot.pool.tables['tags'].delete(
                where={
                    'guild_id': ctx.guild.id,
                    'tag_name': name,
                    'tag_owner': ctx.author.id
                }
            )
            await ctx.send(f"Tag {name} has been deleted.")
        else:
            if not check:
                await ctx.send("You can't remove this tag.")
        
    @tag.command(name='me', hidden=True)
    async def my_tags(self, ctx: Context):
        query = await self.bot.pool.tables['tags'].select(
            'tag_name',
            where={
                'tag_owner': ctx.author.id,
                'guild_id': ctx.guild.id
            }
        )
        e = Embed(color=Color.dark_theme())
        if query:
            for row in query:
                fmt = query[0]['tag_name']
                tag = "".join(fmt)
                e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                e.add_field(name="Tags:", value=tag, inline=True)
                await ctx.send(embed=e)
            else:
                if len(row) == 0 or row is None:
                    await ctx.send("No tags found.")


    @tag.command(name="all", hidden=True)
    async def _tags(self, ctx, *, tags):
        pass

def setup(bot):
    bot.add_cog(Tags(bot))