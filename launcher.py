from core import Amaya
import asyncio

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def main():
    bot = Amaya()
    try:
        bot.loop.run_until_complete(bot.pool_connect())
        bot.run()
    except Exception:
        raise
    finally:
        bot.close()


if __name__ == "__main__":
    main()