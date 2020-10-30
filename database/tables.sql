CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	name TEXT,
	discriminator INTEGER,
	JoinDate INTEGER
);

CREATE TABLE IF NOT EXISTS GuildPrefix (
	GuildID INTEGER PRIMARY KEY,
	Prefix TEXT DEFAULT "??"
);


CREATE TABLE IF NOT EXISTS welcomes (
	guild_id TEXT,
	msg_setter TEXT,
	channel_id TEXT
);