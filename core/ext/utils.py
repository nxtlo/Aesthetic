import discord
from random import randint
from discord.ext.commands import bot
from discord import utils as u


class url:
    """
    a Class for the "Click here" values in Embed
    """
    insta = "[Click Here](https://instagram.com/nxtlo)"
    twitter = "[Click Here](https://twitter.com/helfate)"
    bungie = "[Click Here](https://www.bungie.net/en/Profile/254/20315338/Fate)"
    github = "[Click Here](https://github.com/nxtlo)"
    steam = "[Click Here](https://steamcommunity.com/id/LordhaveFate/)"
    youtube = "[Click Here](https://youtube.com/channel/UC4acY39W-lBjgiqOBsaoqJw)"

class emojis():
    """a Class for custom emojis"""

    #social media emojis

    def insta(self):
        insta = u.get(self.bot.emojis, name="insta")
        return insta

    def twitter(self):
        twitter = u.get(self.bot.emojis, name="twitter")
        return twitter

    def bungie(self):
        bungie = u.get(self.bot.emojis, name="bungie")
        return bungie

    def steam(self):
        steam = u.get(self.bot.emojis, name="steam")
        return steam

    def github(self):
        github = u.get(self.bot.emojis, name="github")
        return github

    def youtube(self):
        utube = u.get(self.bot.emojis, name="youtube")
        return utube

    #utils emojis

    def proc(self):
        proc = u.get(self.bot.emojis, name="processing")
        return proc

    def check(self):
        check = u.get(self.bot.emojis, name="check")
        return check

    def mem(self):
        mem = u.get(self.bot.emojis, name="members")
        return mem

    def mention(self):
        mention = u.get(self.bot.emojis, name="mention")
        return mention

    def boost(self):
        boost = u.get(self.bot.emojis, name="boosters")
        return boost
    
    def setting(self):
        setting = u.get(self.bot.emojis, name="setting")
        return setting

    def plus(self):
        plus = u.get(self.bot.emojis, name="plus")
        return plus

    def dscord(self):
        dscord = u.get(self.bot.emojis, name="d_emoji")
        return dscord

    def dev(self):
        dev = u.get(self.bot.emojis, name="dev")
        return dev

    def mod(self):
        mod = u.get(self.bot.emojis, id='772677329188421632')
        return mod
    
    #-----------

    def custom_status(self):
        custom = u.get(self.bot.emojis, name="customstatus")
        return custom



    def online(self):
        online = u.get(self.bot.emojis, name='online')
        return online
    
    def idle(self):
        idle = u.get(self.bot.emojis, name='idle')
        return idle
    
    def dnd(self):
        dnd = u.get(self.bot.emojis, name='dnd')
        return dnd
    
    def offline(self):
        offline = u.get(self.bot.emojis, name='offline')
        return offline

    

    # roles
class role:
    """class for roles"""

    
    def verified(self, message):
        verified = u.get(message.get.roles, name="Verified")
        return verified


class color:
    "Class for my custom colors"

    def random(self):
        return randint(0, 0xFFFFFF)
    

    def invis(self):
        return 0x36393f