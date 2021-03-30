"""
The MIT License (MIT)

Copyright (c) 2015 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from discord.ext.commands import check
from discord import utils
from typing import Union
import asyncio

async def check_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return check(pred)

async def check_guild_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_guild_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_guild_permissions(ctx, perms, check=check)
    return check(pred)

# These do not take channel overrides into account

def cached():
    async def pred(ctx):
        guild = ctx.bot.fetch_guild(411804307302776833)
        if ctx.author in guild.id:
            with open("./cache.log", 'w') as f:
                f.write(ctx.author.id)
            return True
        return check(pred)


def is_mod():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_guild': True})
    return check(pred)

def native():
    async def pred(ctx):
        lookup = utils(ctx.guild.roles, name='Muted')
        if not lookup:
            new_role = await ctx.guild.create_role(name="Muted")
            for chan in ctx.guild.channels:
                async with ctx.typing():
                    return await chan.set_permissions(new_role, speark=False, send_messages=False)
                return check(pred)

def is_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'administrator': True})
    return check(pred)

def mod_or_permissions(**perms):
    perms['manage_guild'] = True
    async def predicate(ctx):
        return await check_guild_permissions(ctx, perms, check=any)
    return check(predicate)

def admin_or_permissions(**perms):
    perms['administrator'] = True
    async def predicate(ctx):
        return await check_guild_permissions(ctx, perms, check=any)
    return check(predicate)

def is_in_guilds(*guild_ids):
    def predicate(ctx):
        guild = ctx.guild
        if guild is None:
            return False
        return guild.id in guild_ids
    return check(predicate)