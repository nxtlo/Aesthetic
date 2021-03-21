import asyncio
import traceback
import httpx
from . import HTTP
from .ext import *


class Client:
    __slots__ = ('client', 'key', 'loop')
    URL = "https://api.steampowered.com"

    def __init__(self, key = None, client: httpx.AsyncClient = None, loop = None):
        self.key = key
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.client = HTTP(session=client)


    def __repr__(self):
        return "<Client client={0.client} key={0.key}>".format(self)

    def __contains__(self, key):
        return key in self.key

    def __get__(self):
        return self.key

    def __client__(self):
        return self.client

    async def get_bans(self, user: int):
        path = await self.client.get(f"{self.URL}/ISteamUser/GetPlayerBans/v1/?key={self.key}&steamids={user}")
        return VAC(path)

    async def get_user(self, user: int):
        path = await self.client.get(f"{self.URL}/ISteamUser/GetPlayerSummaries/v2/?key={self.key}&steamids={user}")
        return User(path)

    async def get_last_played(self, user: int):
        path = await self.client.get(f"{self.URL}/IPlayerService/GetRecentlyPlayedGames/v1/?key={self.key}&steamid={user}")
        return LastPlayed(path)

    async def get_friends(self, user: int):
        path = await self.client.get(f"{self.URL}/ISteamUser/GetFriendList/v1/?key={self.key}&steamid={user}")
        return Friends(path)

    async def get_news(self, appid: int):
        path = await self.client.get(f"{self.URL}//ISteamNews/GetNewsForApp/v2/?appid={appid}")
        return App(path)


    def run(self, func):
        try:
            self.loop.run_until_complete(func)
        except Exception:
            pass
