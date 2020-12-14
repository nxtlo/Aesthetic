CREATE TABLE IF NOT EXISTS Guilds (
    id INT PRIMARY KEY,
    prefix TEXT DEFAULT "a.",
    guild_name TEXT,
    guild_owner_id INT,
    member_count INT,
    join_date INT
);


CREATE TABLE IF NOT EXISTS bans ( 
    id INT PRIMARY KEY,
    member_id INT,
    author_id INT,
    date INT,
    reason TEXT

);


CREATE TABLE IF NOT EXISTS kicks (
    id INT PRIMARY KEY,
    member_id INT,
    author_id INT,
    date INT,
    reason TEXT
);


CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY,
    Creation_id INT,
    UserName TEXT,
    JoinedAt INT
);

-- this table interact with the append <owner> command.

CREATE TABLE IF NOT EXISTS owners (
    id INT PRIMARY KEY
);