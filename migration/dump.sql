-- Dumped from database version 13.1

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

--
-- Name: show_tables(); Type: FUNCTION; Schema: public; Owner: postgres
--

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

--
-- Name: amaya; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.amaya (
    bot_id bigint NOT NULL,
    owner_id bigint NOT NULL,
    guild_id bigint,
    guilds integer,
    members integer
);


ALTER TABLE public.amaya OWNER TO fate;

--
-- Name: logging; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.logging (
    guild_id bigint NOT NULL,
    logchannel bigint NOT NULL
);


ALTER TABLE public.logging OWNER TO fate;

--
-- Name: prefixes; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.prefixes (
    id bigint NOT NULL,
    prefix text
);


ALTER TABLE public.prefixes OWNER TO fate;

--
-- Name: staff; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.staff (
    staff_id bigint NOT NULL,
    became_at text,
    guild_id bigint
);


ALTER TABLE public.staff OWNER TO fate;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.tags (
    guild_id bigint NOT NULL,
    tag_name text,
    created_at timestamp with time zone DEFAULT timezone('UTC'::text, now()) NOT NULL,
    tag_id text NOT NULL,
    tag_owner bigint NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.tags OWNER TO fate;

--
-- Name: warns; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.warns (
    guild_id bigint NOT NULL,
    warn_id text NOT NULL,
    member_id bigint,
    author_id bigint,
    reason text,
    warned_at timestamp with time zone DEFAULT timezone('UTC'::text, now()) NOT NULL
);


ALTER TABLE public.warns OWNER TO fate;

COPY public.amaya (bot_id, owner_id, guild_id, guilds, members) FROM stdin;

COPY public.logging (guild_id, logchannel) FROM stdin;

COPY public.prefixes (id, prefix) FROM stdin;

COPY public.staff (staff_id, became_at, guild_id) FROM stdin;

COPY public.tags (guild_id, tag_name, created_at, tag_id, tag_owner, content) FROM stdin;

COPY public.warns (guild_id, warn_id, member_id, author_id, reason, warned_at) FROM stdin;


ALTER TABLE ONLY public.amaya
    ADD CONSTRAINT amaya_pkey PRIMARY KEY (bot_id);


ALTER TABLE ONLY public.logging
    ADD CONSTRAINT logging_pkey PRIMARY KEY (guild_id);



ALTER TABLE ONLY public.prefixes
    ADD CONSTRAINT prefixes_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);


ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_id);

ALTER TABLE ONLY public.warns
    ADD CONSTRAINT warns_pkey PRIMARY KEY (warn_id);


--
-- PostgreSQL database dump complete
--