# R.Fate

*This is my personal bot, inspired by RoboDanny. :)*


## Setup
* You need python >= 3.8 to run without issues
* Go to [/data/token.txt](https://github.com/nxtlo/R.Fate/blob/master/data/token.txt) and paste youe token there
* `python3.8 -m venv venv`

Then activate by doing this, __actually required to run the bot__

* for windows so this `venv\Scripts\activate.bat`
* for mac and linux do this `source venv/bin/activate`

* now do `pip install -U requirements.txt`

## Running the bot

type `python launcher.py` to run the bot without restart command

run `launhcher.sh` if you want to use the `restart` command

the bot prefix is `??` you can change it from [/core/bot.py](https://github.com/nxtlo/R.Fate/blob/490a9859d61d552aceb18c24bfdf3ea6c8128f5c/core/bot.py#L39)


## Notes 

* the `database.db` file will create it self when you run the bot for the first time

## to-do

- [ ] Leveling sys
 * Probably not going to make it cuz useless :)
 
- [ ] Economy sys _WHERE_ commands _LIKE_ `add balance` `show balance` `transfer balance`

- [ ] Storing guild stuff

- [x] Custom prefixes

- [ ] Prefixes per guild

- [ ] Logging bans/kicks/mutes
