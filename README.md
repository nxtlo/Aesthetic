# Amaya

*my personal discord bot*
You can [invite](https://discord.com/oauth2/authorize?client_id=760052204777504778&permissions=0&scope=bot) my bot from here.

## hosting the bot yourself

* You need python 3.8 to run without issues
* Go to `data/example_config.py` and rename to `config.py` then paste your tokens there

## venv setup

* On windows do `py -3.8 -m venv venv`
* On mac and linux do this `python3.8 -m venv venv`

Then activate by doing this, _Actually required to run the bot_

* for windows do this `venv\Scripts\activate.bat`
* for mac and linux do this `source venv/bin/activate`

* now do `python -m pip install -U -r requirement.txt`

## Running the bot

* windows: `py -3.8 launcher.py`
* Linux/Mac: `python3.8 launcher.py`

## Notes

After running the bot for the first time, i highly suggest running this command `@YourBot db init`

The bot prefix is `a.` you can change it using `set prefix <prefix>` command