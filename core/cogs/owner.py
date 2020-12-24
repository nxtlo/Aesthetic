from discord.ext.commands import Cog, is_owner,command, ExtensionError, group
from contextlib import redirect_stdout
from discord import Embed, Member
from core.ext import utils as ej
from data import db
from .commands import FetchedUser
from ..ext.utils import color

    ### Red-bot api for botstats command and listguilds

from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, close_menu
from redbot.core.utils.common_filters import filter_invites
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import chat_formatting as cf

import typing
import asyncio
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

    # command under is not mine -> aikaterna-cogs / redbot-core


    @command(name="listguilds", aliases=["listservers", "guildlist", "serverlist", "lsg"], hidden=True)
    @is_owner()
    async def listguilds(self, ctx):
        """servers the bot is in."""
        asciidoc = lambda m: "```asciidoc\n{}\n```".format(m)
        guilds = sorted(self.bot.guilds, key=lambda g: -g.member_count)
        header = ("```\n" "The bot is in the following {} server{}:\n" "```").format(
            len(guilds), "s" if len(guilds) > 1 else ""
        )

        max_zpadding = max([len(str(g.member_count)) for g in guilds])
        form = "{gid} :: {mems:0{zpadding}} :: {name}"
        all_forms = [
            form.format(
                gid=g.id,
                mems=g.member_count,
                name=filter_invites(cf.escape(g.name)),
                zpadding=max_zpadding
            )
            for g in guilds
        ]
        final = "\n".join(all_forms)

        await ctx.send(header)
        page_list = []
        for page in cf.pagify(final, delims=["\n"], page_length=1000):
            page_list.append(asciidoc(page))

        if len(page_list) == 1:
            return await ctx.send(asciidoc(page))
        await menu(ctx, page_list, DEFAULT_CONTROLS)



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
            db.con.close()
            await self.bot.logout()
            
        except ConnectionError as e:
            raise e


def setup(bot):
    bot.add_cog(Owner(bot))
