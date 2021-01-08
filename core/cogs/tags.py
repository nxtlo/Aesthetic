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


from ..ext.utils import color
from discord.ext.commands import command, Cog, group, Context
from discord import Embed, Member, Color
from typing import Optional
from uuid import uuid4
from datetime import datetime
from ..ext.converters import convert


# this is a simple tag system nothing interesting to see here.


class Tags(Cog, name="\U0001f4cc Tags"):
    '''Commands related to Tags.'''
    _slots_ = ('me', 'add', 'create', 'remove', 'edit', 'info')

    def __init__(self, bot):
        self.bot = bot



    @group(invoke_without_command=True)
    async def tag(self, ctx, *, name):
        fetched = await self.bot.pool.fetch('''
                                            SELECT content, tag_name
                                            FROM tags 
                                            WHERE tag_name = $1 AND guild_id = $2''',
                                            name, ctx.guild.id)

        if not name in fetched:
            return
        else:
            content = [c['content'] for c in fetched]
            await ctx.send(*content)

    @tag.command(aliases=['create'])
    async def add(self, ctx: Context, name, *, content: str = None):
        """Creates a new tag."""
        
        if name in self._slots_:
            return
        
        if content is None:
            return await ctx.send("You're missing the content.")

        istag = await self.bot.pool.fetch(
                                        '''
                                        SELECT tag_name
                                        FROM tags
                                        WHERE tag_name = $1 AND guild_id = $2
                                        ''', name, ctx.guild.id
                                    )
        exists = [t['tag_name'] for t in istag]

        if not name in exists:
            query = '''INSERT INTO tags(guild_id, tag_name, created_at, tag_id, tag_owner, content) VALUES($1, $2, $3, $4, $5, $6)'''
            await self.bot.pool.execute(query, 
                                        ctx.guild.id, 
                                        name, 
                                        datetime.utcnow(), 
                                        str(uuid4())[:8], 
                                        ctx.author.id, 
                                        content)
            await ctx.send(f"Created tag `{name}`")
        else:
            return await ctx.send("Tag name already taken.")



    @tag.command(name='remove')
    async def rem_tag(self, ctx, *, name):
        """Removes a tag by its name."""
        check = await self.bot.pool.fetch(
            '''SELECT tag_owner, tag_name  
               FROM tags 
               WHERE tag_owner = $1 
               AND guild_id = $2''', 
               ctx.author.id, ctx.guild.id)
        
        Name = [t['tag_name'] for t in check]
        
        if not name in Name:
            return await ctx.send("No tag found.")
        else:
            if check or ctx.author.id == self.bot.fate:
                await self.bot.pool.execute(
                    '''
                    DELETE FROM tags
                    WHERE tag_name = $1
                    ''', name
                )
                await ctx.send(f"Tag {name} has been deleted.")
            else:
                await ctx.send("You can't remove this tag.")


    @tag.command(name='me', hidden=True)
    async def my_tags(self, ctx: Context):
        """Shows your own tags."""
        query = await self.bot.pool.fetch("SELECT * FROM tags WHERE guild_id = $1", ctx.guild.id)

        if len(query) == 0 or query is None:
            await ctx.send("No tags found.")
        else:
            fmt = '\n'.join(tag['tag_name'] + ' ' + f"(ID: {tag['tag_id']})" for tag in query)
            e = Embed(color=Color.dark_theme(), description=fmt)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)


    @tag.command(name="edit")
    async def _edit(self, ctx, tag, *, new):
        """Edits your tag."""
        checks = await self.bot.pool.fetch(
                     '''SELECT tag_owner, tag_name
                        FROM tags
                        WHERE tag_owner = $1
                        AND tag_name = $2
                     ''', ctx.author.id, tag)
        try:
            NotFound = [t['tag_name'] for t in checks]
            if not tag in NotFound:
                await ctx.send("Tag not found.")
            elif checks:
                query = '''
                        UPDATE tags
                        SET content = $1
                        WHERE tag_name = $2
                        AND guild_id = $3
                        '''
                await self.bot.pool.execute(query, new, tag, ctx.guild.id)
                await ctx.send("Tag edited.")
            else:
                pass
        except Exception:
            raise



    @tag.command(name='info', aliases=['about'])
    async def _tag_info(self, ctx, *, tag):
        '''returns info about a specific tag.'''
        
        found = await self.bot.pool.fetchrow('''SELECT tag_name, tag_owner, created_at, tag_id 
                                             FROM tags WHERE tag_name = $1 AND guild_id = $2''',tag, ctx.guild.id)
        if found:
            name = found['tag_name']
            owner = f'<@{found["tag_owner"]}>'
            created_at = found['created_at']
            tag_id = found['tag_id']

            e = Embed(title=f"Info about {tag}", color=color.invis(self))
            e.add_field(name='Name', value=name)
            e.add_field(name='Owner', value=owner)
            e.add_field(name='ID', value=tag_id)
            e.add_field(name='Created At', value=created_at)
            await ctx.send(embed=e)
        else:
            await ctx.send('Tag not found.')

def setup(bot):
    bot.add_cog(Tags(bot))