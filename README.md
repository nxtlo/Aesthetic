# Amaya

*my personal discord bot*
You can [invite](https://discord.com/oauth2/authorize?client_id=760052204777504778&permissions=0&scope=bot) my bot from here.

## hosting the bot yourself

* Postrges 9.5 or higher
* You need python 3.8 to run without issues
* Go to `data/example_config.py` and rename to `config.py` then paste your configs there


## Database Setup

Just type in psql this:

```sql
CREATE ROLE ? WITH LOGIN PASSWORD 'yourpass';
CREATE DATABASE ? OWNER ?;
ALTER USER ? WITH SUPERUSER;
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

### Optional

if you want to Recreate the database tables just type `a.db init`