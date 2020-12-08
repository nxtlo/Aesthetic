# Aesthetic

*my personal discord bot*
Invite Link [invite](https://discord.com/oauth2/authorize?client_id=760052204777504778&permissions=0&scope=bot) my bot as well :)

## hosting the bot

* You need python >= 3.8 to run without issues
* Go to `data/example_token.txt` and rename the file to `token.txt` then paste your token in the file

## venv setup

* On windows do `py -3.8 -m venv venv`

* On mac and linux do this `python3.8 -m venv venv`

Then activate by doing this, __Actually required to run the bot__

* for windows do this `venv\Scripts\activate.bat`
* for mac and linux do this `source venv/bin/activate`

* now do `pip install -U -r requirements.txt`

## Running the bot

run `python3.8 launcher.py` to run the bot without restart command

run `launhcher.sh` for `restart` command support

The bot prefix is `ae>` you can change it using `set prefix <prefix>`


## Notes 

* the `database.db` file will create it self when you run the bot for the first time

* if you run the bot for the first time, i highly suggest running this command `@YourBot db init`