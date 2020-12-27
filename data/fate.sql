--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
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
-- Name: guilds; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.guilds (
    id character varying(36) NOT NULL,
    members text,
    owner text
);


ALTER TABLE public.guilds OWNER TO fate;

--
-- Name: logging; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.logging (
    id character varying(36) NOT NULL,
    logchannel text
);


ALTER TABLE public.logging OWNER TO fate;

--
-- Name: prefixes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prefixes (
    id character varying(36) NOT NULL,
    prefix text
);


ALTER TABLE public.prefixes OWNER TO postgres;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: fate
--

CREATE TABLE public.tags (
    guild_id character varying(36) NOT NULL,
    tag_name text,
    tag_owner text,
    content text
);


ALTER TABLE public.tags OWNER TO fate;

--
-- Data for Name: guilds; Type: TABLE DATA; Schema: public; Owner: fate
--

COPY public.guilds (id, members, owner) FROM stdin;
\.


--
-- Data for Name: logging; Type: TABLE DATA; Schema: public; Owner: fate
--

COPY public.logging (id, logchannel) FROM stdin;
411804307302776833	789614938247266305
781336284424699906	790061828474404894
758236292415881217	785904530374131773
\.


--
-- Data for Name: prefixes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prefixes (id, prefix) FROM stdin;
637708272555786260	a.
781336284424699906	a.
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: fate
--

COPY public.tags (guild_id, tag_name, tag_owner, content) FROM stdin;
411804307302776833	phonky	350750086357057537	til
\.


--
-- Name: guilds guilds_pkey; Type: CONSTRAINT; Schema: public; Owner: fate
--

ALTER TABLE ONLY public.guilds
    ADD CONSTRAINT guilds_pkey PRIMARY KEY (id);


--
-- Name: logging logging_pkey; Type: CONSTRAINT; Schema: public; Owner: fate
--

ALTER TABLE ONLY public.logging
    ADD CONSTRAINT logging_pkey PRIMARY KEY (id);


--
-- Name: prefixes prefixes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prefixes
    ADD CONSTRAINT prefixes_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: fate
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (guild_id);


--
-- PostgreSQL database dump complete
--

