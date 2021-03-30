from uuid import uuid4
from discord.ext.commands import command, group, Cog
from discord import Embed, Member
from typing import Optional


class Profiles(Cog, name="\U0001f4c7 Profiles"):
    """Custom profile for the members."""
    def __init__(self, bot):
        self.bot = bot
        self._slots = ('info', 'age', 'country', 'city', 'gender', 'relation',)


    @group(invoke_without_command=True)
    async def profile(self, ctx, member: Optional[Member] = None):
        '''
        Show you information about your profile, 
        if your don't have one, Please type `profile create`
        '''
        member = member or ctx.author
        try:
            query = await self.bot.pool.fetchval('SELECT member_id FROM profiles WHERE member_id = $1', member.id)
            if not query:
                return await ctx.send(f"Profile for {member.name} not found, if you don't have a profile just type {ctx.prefix}profile create.")
            else:
                _profile = await self.bot.pool.fetchrow("SELECT * FROM profiles WHERE member_id = $1", member.id)
                e = Embed(description=_profile['info'] if _profile['info'] else None, color=member.color)
                field = e.add_field
                e.set_author(name=_profile['_name'], icon_url=_profile['avatar'])
                field(name='Profile id', value=_profile['profile_id'], inline=True)
                field(name='Member id', value=_profile['member_id'], inline=True)
                field(name='Relationship', value=_profile['relation'], inline=False)
                field(name='Gender', value=_profile['gender'], inline=True)
                field(name='Age', value=_profile['age'], inline=True)
                field(name='Country', value=_profile['country'], inline=True)
                field(name='City', value=_profile['city'], inline=True)
                e.set_thumbnail(url=_profile['avatar'])
                await ctx.send(embed=e)
        except Exception as e:
            raise e

    @profile.command(name='options')
    async def _options(self, ctx):
        '''Shows the available options for the profile '''
        __options = '''
        Usage:
        profile set `option` `arguments`

        Exmaple:
        profile name Fate
        profile city Berlin

        Options:
        info -> Description about your current profile
        age  -> Your age
        country -> Your country
        city -> Your city
        gender -> Your gender
        relation -> Your relationship
        '''
        e = Embed(description=__options)
        await ctx.send(embed=e)


    @profile.command(name='purge', aliases=['clear', 'delete'])
    async def del_profile(self, ctx, profile_id: int) -> None:
        '''Removes a profile.'''
        profile = profile_id or ctx.author.id
        try:
            check = await self.bot.pool.fetchval("SELECT member_id FROM profiles WHERE member_id = $1", ctx.author.id)
            check = check or ctx.author.id == self.bot.fate
            if not check:
                return await ctx.send("You can't delete this profile.")
            else:
                await self.bot.pool.execute("DELETE FROM profiles WHERE member_id = $1", profile)
                await ctx.send(f"Done.")
        except Exception as e:
            raise e


    @profile.command(name='create', aliases=['init'], hidden=True)
    async def init_profile(self, ctx):
        '''Creates a profile for you.'''

        if ctx.author.bot:
            return

        check = await self.bot.pool.fetchval("SELECT member_id FROM profiles WHERE member_id = $1", ctx.author.id)
        if not check:
            query = '''
                    INSERT INTO profiles(profile_id, member_id, _name, relation, country, city, age, gender, info, avatar)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    '''
            await self.bot.pool.execute(query, str(uuid4())[:8], ctx.author.id, ctx.author.name, None, None, None, None, None, None, str(ctx.author.avatar_url))
            await ctx.send(f"Created your profile, type `{ctx.prefix}profile` to view it, type {ctx.prefix}profile options to edit your profile.")
        else:
            return

    @profile.command(name='name')
    async def _name(self, ctx, *, name: str = None):
        '''Sets your profile name.'''
        if not name:
            name = ctx.author.name
        try:
            query = 'UPDATE profiles SET _name = $1 WHERE member_id = $2'
            await self.bot.pool.execute(query, name, ctx.author.id)
            await ctx.send(f'Updated profile name to {name}')
        except Exception as e:
            await ctx.send(e)

    @profile.command(name='age')
    async def _age(self, ctx, *, age: int):
        '''Sets your profile age.'''
        query = 'UPDATE profiles SET age = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, age, ctx.author.id)
        await ctx.send(f'Updated profile age to {age}')


    @profile.command(name='gender')
    async def _gender(self, ctx, *, gender: str):
        '''Sets your profile gender.'''
        query = 'UPDATE profiles SET gender = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, gender, ctx.author.id)
        await ctx.send(f'Updated profile Gender to {gender}')


    @profile.command(name='city')
    async def _city(self, ctx, *, city: str):
        '''Sets your profile city.'''
        query = 'UPDATE profiles SET city = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, city, ctx.author.id)
        await ctx.send(f'Updated profile City to {city}')


    @profile.command(name='country')
    async def _country(self, ctx, *, country: str):
        '''Sets your profile country'''
        query = 'UPDATE profiles SET country = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, country, ctx.author.id)
        await ctx.send(f'Updated profile Country to {country}')


    @profile.command(name='relation')
    async def _relation(self, ctx, *, relation: str):
        '''Sets your profile relationship.'''
        query = 'UPDATE profiles SET relation = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, relation, ctx.author.id)
        await ctx.send(f'Updated profile Relationship to {relation}')


    @profile.command(name='info')
    async def _info(self, ctx, *, info: str = None) -> None:
        '''Sets the description of your profile or/and info about you.'''
        query = 'UPDATE profiles SET info = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, info, ctx.author.id)
        await ctx.send(f"Updated profile information to {info}")


    @profile.command(name='avatar')
    async def _avatar(self, ctx, url: str = None):
        url = url or ctx.author.avatar_url
        query = 'UPDATE profiles SET avatar = $1 WHERE member_id = $2'
        await self.bot.pool.execute(query, url, ctx.author.id)
        await ctx.send("Profile avatar set.")

def setup(bot):
    bot.add_cog(Profiles(bot))