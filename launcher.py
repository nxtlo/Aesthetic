from core import MainBot

def main():
    bot = MainBot()
    bot.remove_command("help")
    bot.run()


if __name__ == "__main__":
    main()