from discord.ext.commands import has_any_role, has_guild_permissions, has_role


    # you can change the roles numbers to yours btw

def is_mod():
    is_mod = has_any_role(757715657054748713, 757714978911420497)
    return is_mod


def is_admin():
    is_admin = has_guild_permissions(administrator=True)
    return is_admin


def is_manager():
    is_manager = has_guild_permissions(manage_guild=True)
    return is_manager

    # same thing

def is_vip():
    is_vip = has_role(587566458217955349)
    return is_vip