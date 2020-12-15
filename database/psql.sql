-- an entry for future psql database

CREATE ROLE fate 
    WITH LOGIN PASSWORD '';
CREATE EXTENSION pg_trgm;

CREATE DATABASE fate
    WITH OWNER = fate
ENCODING = 'UTF8'
TABLESPACE = pg_default
CONNECTION LIMIT = -1;

CREATE TABLE IF NOT EXISTS public.guilds (
    g_id    VARCHAR NOT NULL,
    g_name  TEXT NOT NULL,
    g_members VARCHAR NOT NULL,
CONSTRAINT guilds_pkey PRIMARY KEY (g_id) 
);

CREATE TABLE IF NOT EXISTS prefixes (
    p_id    VARCHAR NOT NULL,
    prefix  VARCHAR DEFAULT 'a.' NOT NULL
    
);

ALTER TABLE public.guilds
    OWNER to postgres;

ALTER TABLE public.prefixes
    ADD COLUMN
        prefix VARCHAR COLLATE;