CREATE TABLE IF NOT EXISTS tags (
    guild_id BIGINT NOT NULL,
    tag_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    tag_id TEXT PRIMARY KEY,
    tag_owner BIGINT NOT NULL,
    content TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS warns (
    guild_id BIGINT NOT NULL,
    warn_id TEXT PRIMARY KEY,
    member_id BIGINT,
    author_id BIGINT,
    reason TEXT,
    warned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')

);

CREATE TABLE IF NOT EXISTS prefixes (
    id BIGINT PRIMARY KEY,
    prefix TEXT
);


CREATE TABLE IF NOT EXISTS logging (
    guild_id BIGINT PRIMARY KEY,
    logchannel BIGINT NOT NULL
);