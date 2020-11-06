CREATE TABLE IF NOT EXISTS Guilds (
    id INT PRIMARY KEY,
    guild_name TEXT,
    guild_owner_id INT,
    member_count INT,
    join_date INT
);


CREATE TABLE IF NOT EXISTS bans ( 
    Guild_Name TEXT,
    member_id INT,
    author_id INT,
    date INT,
    reason TEXT

);


CREATE TABLE IF NOT EXISTS kicks (
    Guild_name TEXT,
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