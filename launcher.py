from core import Aesthetic

def main():
    bot = Aesthetic()
    bot.remove_command("help")
    bot.run()


if __name__ == "__main__":
    main()