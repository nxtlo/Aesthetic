import httpx

class HTTP:
    __slots__ = ('session',)
    def __init__(self, *, session: httpx.AsyncClient = None):
        self.session = session 

    async def create(self):
        self.session = httpx.AsyncClient()

    async def get(self, url):
        if not self.session:
            await self.create()

        async with httpx.AsyncClient() as cl:
            data = await cl.get(url, headers={})
            try:
                return data.json()
            except httpx.DecodingError:
                return data.text

    async def close(self):
        if not self.session.is_closed:
            await self.session.aclose()
            self.session = None
