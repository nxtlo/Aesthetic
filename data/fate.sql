-- Dumped by pg_dump version 13.1
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE FUNCTION public.show_tables() RETURNS SETOF text
    LANGUAGE sql
    AS $$
        SELECT
            table_name
        FROM
            information_schema.tables
        WHERE
            table_type = 'BASE TABLE'
        AND
            table_schema NOT IN ('pg_catalog', 'information_schema');
        $$;


ALTER FUNCTION public.show_tables() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.prefixes (
    id character varying(36) NOT NULL,
    prefix text
);


ALTER TABLE public.prefixes OWNER TO fate;

CREATE TABLE public.tags (
    guild_id text,
    tag_name text,
    created_at text,
    tag_id character varying(36) NOT NULL,
    tag_owner text,
    content text,
    jumpurl text
);


ALTER TABLE public.tags OWNER TO fate;

CREATE TABLE public.warns (
    guild_id text,
    warn_id character varying(36) NOT NULL,
    member_id text,
    author_id text,
    reason text,
    date text
);


ALTER TABLE public.warns OWNER TO fate;


COPY public.prefixes (id, prefix) FROM stdin;
\.

COPY public.tags (guild_id, tag_name, created_at, tag_id, tag_owner, content, jumpurl) FROM stdin;
\.

COPY public.warns (guild_id, warn_id, member_id, author_id, reason, date) FROM stdin;
\.



ALTER TABLE ONLY public.prefixes
    ADD CONSTRAINT prefixes_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_jumpurl_key UNIQUE (jumpurl);

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_id);

ALTER TABLE ONLY public.warns
    ADD CONSTRAINT warns_pkey PRIMARY KEY (warn_id);