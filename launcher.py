from core import Amaya
from core.ext import PgPool
import asyncio

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def main() -> None:
    run = asyncio.get_event_loop().run_until_complete
    pool = run(PgPool().__ainit__())
    bot = Amaya()
    bot.pool = pool
    bot.run()

if __name__ == "__main__":
    main()