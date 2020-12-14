import discord
from discord.ext.commands import command, Cog, group
import random



class Git(Cog, name="\U0001f4c1 git"):
    def __init__(self, bot):
        self.bot = bot



    @group(name="git")
    async def git(self, ctx):
        """```Useage user: git user <username>```\n```Useage repo: git repo <username> <reponame>```"""
        pass


    @git.command(name="user")
    async def user_command(self, ctx, *, user: str):
        
        try:
            name = user.replace(" ", "+")
            github = "https://github.com/" + name
            await ctx.send(github)
        
        except Exception as e:
            if user is None:
                await ctx.send("Please provide a user" + e)


    @git.command(name="repo")
    async def repo_command(self, ctx, user: str, *, repo: str):
        if user is None:
            await ctx.send("Please provide a user or type `pls git` for more info")
        elif repo is None:
            await ctx.send("Please provide a repo name or type `pls git` for more info")
        
        else:
            repo = repo.replace(" ", "+")
            repo_link = "https://github.com/" + user + "/" + repo
            await ctx.send(repo_link)
        
def setup(bot):
    bot.add_cog(Git(bot))