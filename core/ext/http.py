import httpx
from typing import Optional


class HTTPClient:
    __slots__ = ('session',)

    def __init__(self, session: httpx.AsyncClient = None):
        self.session = session
    
    async def session_init(self):
        self.session = httpx.AsyncClient()

    async def get(self, url, **kwargs):
        if not self.session:
            await self.session_init()

        async with self.session as client:
            data = await client.get(url, **kwargs)
            try:
                return data.json()
            except Exception:
                return data.text

    async def close(self):
        if not self.session.is_closed:
            await self.session.aclose()
            self.session = None