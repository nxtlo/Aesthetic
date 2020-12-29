"""
MIT License

Copyright (c) 2020 nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""



from discord.ext.commands import command, Cog, group, Context
from discord import Embed, Member, Color
from typing import Optional


# this is a simple tag system nothing interesting to see here.

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
                return
            else:
                for t in tag:
                    fmt = t = "".join((str(t).replace("{","").replace("}", "").replace("'content': ", "").replace("'", "").replace("'", "")))
                await ctx.send(f"{fmt}")
        except Exception:
            return None

    @tag.command(aliases=['new', 'create'])
    async def add(self, ctx, name, *, content):
        """Creates a new tag."""
        if name and content is not None:
            if content is None:
                await ctx.send("You're missing the content.")
        await self.bot.pool.tables['tags'].insert(
            guild_id=ctx.guild.id,
            tag_name=name,
            tag_owner=ctx.author.id,
            content=content
        )
        await ctx.send(f"Created tag `{name}`")


    @tag.command(name='remove', aliases=['del', 'rem'])
    async def rem_tag(self, ctx, *, name):
        """Removes a tag"""
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
            if ctx.author.id not in check:
                await ctx.send("You can't remove this tag.")
        
    @tag.command(name='me', hidden=True)
    async def my_tags(self, ctx: Context):
        """Shows your own tags."""
        query = await self.bot.pool.tables['tags'].select(
            'tag_name',
            where={
                'tag_owner': ctx.author.id,
                'guild_id': ctx.guild.id
            }
        )
        e = Embed(color=Color.dark_theme())
        
        if len(query) == 0 or query is None:
            await ctx.send("No tags found.")
        else:
            fmt = query[0]['tag_name']
            tag = "".join(fmt)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            e.add_field(name="Tags:", value=tag, inline=True)
            await ctx.send(embed=e)

    
    @tag.command(name="edit")
    async def _edit(self, ctx, tag, *, new):
        """Edits your tag."""
        check = await self.bot.pool.tables['tags'].select(
            'tag_owner',
            where={
                'tag_owner': ctx.author.id
            }
        )
        try:
            if check:
                await self.bot.pool.tables['tags'].update(
                    content=new,
                    where={
                        'tag_name': tag,
                        'guild_id': ctx.guild.id
                    }
                )
                await ctx.send("Tag edited.")
            else:
                return await ctx.send("You can't edit this tag.")
        except Exception:
            raise



    @tag.command(name='info', aliases=['about'])
    async def _tag_info(self, ctx, *, tag):
        '''returns info about a specific tag.'''
        pass

def setup(bot):
    bot.add_cog(Tags(bot))