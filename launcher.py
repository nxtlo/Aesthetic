from core import Amaya

def main():
    bot = Amaya()
    bot.loop.run_until_complete(bot.pool_connect())
    bot.run()


if __name__ == "__main__":
    main()