from ..ext.utils import color
from discord.ext import fancyhelp
from discord.ext.commands import Cog


class Help(Cog, name="\U00002699 Help"):
    """ Help commands """

    def __init__(self, bot):
        self._original_help_command = bot.help_command


        bot.help_command = fancyhelp.EmbeddedHelpCommand(color=color.invis(self))
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command
        self.bot.help_command.cog = self._original_help_command.cog

# Cog setup
def setup(bot):
    bot.add_cog(Help(bot))