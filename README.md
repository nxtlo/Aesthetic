# Amaya

Amaya is a my only public discord bot, 
it was created for general usage like moderation, apis and other fun stuff.
[invite](https://discord.com/oauth2/authorize?client_id=760052204777504778&permissions=0&scope=bot) Link

## Hosting the bot yourself

* Postrges >=9.5
* You need python >=3.8 to run without issues
* Go to `data/example_config.py` and rename to `config.py` then this configs

```py
bot_token='THE BOT TOKEN'
bungie_key = 'BUNGIE API KEY'
weather_api='OPEN WEATHER API KEY'
database = '' # your database name
db_user = '' # your database username
password = '' # your database password
host = '' # your database host -- Default is localhost
port = 5432 # your database port -- Default is 5432
rapid_api = 'RAPID API KEY FOR URBAN DICT' # Check this here https://rapidapi.com/community/api/urban-dictionary
```

## Database Setup

Just type in psql this:

```sql
CREATE ROLE YourName WITH LOGIN PASSWORD 'yourpass';
CREATE DATABASE DBName OWNER YourName;
ALTER USER YourName WITH SUPERUSER;
```


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

### Cython

Amaya currently have some experiential C / Cython code
if you don't wanna deal with this just go to `launcher.py` and remove the `build_c()` from `main()`
otherwise you will have to build the extension by running this `python launcher.py buiild_ext -i`

## Optional

if you want to rebuild the database tables just run this command `a.db init`