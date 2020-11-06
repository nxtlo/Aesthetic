import discord
from discord.ext.commands import command, Cog, group
import random



class git(Cog, name="<a:github:767576538823524363> git"):
    def __init__(self, bot):
        self.bot = bot



    @group(name="git")
    async def git(self, ctx):
        """Type `pls git help` for commands's usage"""
        pass

    @git.command(name="help")
    async def git_help(self, ctx):
        usage = "```Useage user: git user <username>```\n```Useage repo: git repo <username> <reponame>```"
        
        e = discord.Embed(title="Usage", description=usage, color=0x36393f)
        
        await ctx.send(embed=e)

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
    bot.add_cog(git(bot))