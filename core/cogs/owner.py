from discord.ext.commands import Cog, is_owner,command, ExtensionError, group
from contextlib import redirect_stdout
from discord import Embed, Member, TextChannel, Guild
from core.ext import utils as ej, check
from .commands import FetchedUser
from ..ext.utils import color
from data import config


import typing
import asyncio
import subprocess
import time, datetime
import ast
import inspect
import io
import textwrap
import traceback
import os, inspect



class Owner(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._owner_ids = 350750086357057537


    @command(name='eval', aliases=['try'], hidden=True)
    @is_owner()
    async def _eval(self, ctx, *, body):
        """Evaluates python code"""
        env = {
            'ctx': ctx,
            'bot': self.bot,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            return content.strip('` \n')

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')

    
    @group(hidden=True, invoked_without_command=True)
    async def db(self, ctx):
        """Commands for returning stuff from the database"""
        pass

    @db.command(name='init', hidden=True)
    @is_owner()
    async def _init_(self, ctx):
        '''
        Recreate the database tables,
        You can use the command if you want to recreate the tables without restarting the bot.
        '''
        async with ctx.typing():
            with open('./data/schema.sql', 'r', encoding='utf8') as schema:
                async with ctx.pool.acquire() as conn:
                    try:
                        await conn.execute(schema.read())
                        await ctx.send("\U00002705")
                    except Exception as e:
                        await ctx.send(f"```\n{e}\n```")
                    finally:
                        await ctx.pool.release(conn)


    @db.command(name='sql', aliases=['query', 'sqlx'], hidden=True)
    @is_owner()
    async def run_query(self, ctx, *, query):
        '''runs sql querys.'''
        if not query:
            return
        else:
            reslut = await ctx.pool.fetch(query)
            await ctx.send(f"```\n{reslut}\n```")


    @db.command(name="table", aliases=['info'], hidden=True)
    @is_owner()
    async def _pragma(self, ctx, *, table: str):
        """
        Format the table and render it as rST format
        this command access your psql commandline
        """
        try:
            async with ctx.typing():
                cmd = f'psql -U {config.db_user} -d {config.database} -c "\d {table}"'
                result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if table:
                    if len(cmd) < 2000:
                        await ctx.send(f"```\n{result.communicate()[0]}\n```")
        except Exception:
            raise
        finally:
            pass
    
    @db.command(name="schema", hidden=True)
    @is_owner()
    async def _schema(self, ctx):
        """Show the database schema from psql"""
        try:
            async with ctx.typing():
                cmd = f'psql {config.db_user} {config.database} -c "\dt"'
                schema = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    e = Embed(description=f"```sql\n{schema.communicate()[0]}\n```")
                    await ctx.send(embed=e)
        except Exception as e:
            raise e
    
    @db.command(name="rows", hidden=True)
    @is_owner()
    async def _rows(self, ctx, *, column: str):
        """View table rows from psql"""
        try:
            async with ctx.typing():
                cmd = f'psql {config.db_user} {config.database} -c "SELECT * FROM {column};"'
                rows = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True, encoding='utf8')
                if len(cmd) < 2000:
                    await ctx.send(f"```sql\n{rows.communicate()[0]}\n```")
        except Exception as e:
            raise e


    @command(hidden=True)
    @is_owner()
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try:
            self.bot.load_extension(f"core.cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f"Loaded extension **{name}.py**")

    @command(hidden=True)
    @is_owner()
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        try:
            self.bot.unload_extension(f"core.cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f"Unloaded extension **{name}.py**")

    @command(hidden=True)
    @is_owner()
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.reload_extension(f"core.cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f"Reloaded extension **{name}.py**")


    @command(name='listextensions', aliases=['le'], hidden=True)
    @is_owner()
    async def list_extensions(self, ctx):
        extensions_dict = self.bot.extensions
        msg = '```css\n'

        extensions = []

        for b in extensions_dict:
            # print(b)
            extensions.append(b)

        for a in range(len(extensions)):
            msg += f'{a}: {extensions[a]}\n'

        msg += '```'
        await ctx.send(msg)


    @command(name='shutdown' ,discription="Shutdown the bot", hidden=True)
    @is_owner()
    async def _shutdown(self, ctx):
        try:
            embed = Embed(
                title=f"*Shutting down...*",
                timestamp=ctx.message.created_at
            )
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=embed)
            await self.bot.close()
            
        except ConnectionError as e:
            raise e
    
    @command(name="say", hidden=True)
    @is_owner()
    async def _say(self, ctx, chan: TextChannel=None, *, msg):
        chan = chan or chan.id
        try:
            if not chan:
                await ctx.send(msg)
            await chan.send(msg)
        except Exception:
            raise



def setup(bot):
    bot.add_cog(Owner(bot))
