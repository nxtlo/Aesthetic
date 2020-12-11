"""
Main Database Module,
Creds for :Parafoxia#1911 / :Carberra
"""

from os.path import isfile
from sqlite3 import connect

DB_PATH = "./database/database.db"
BUILD_PATH = "./database/sqhema.sql"


con = connect(DB_PATH, check_same_thread=False)
cur = con.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

def commit():
    con.commit()

def close():
    con.close()

def field(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()

def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()

def coloumn(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]

def execute(command, *values):
    cur.execute(command, tuple(values))

def multiexec(command, valueset):
    cur.execute(command, valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())