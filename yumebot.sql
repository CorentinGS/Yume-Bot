--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Debian 12.3-1.pgdg100+1)
-- Dumped by pg_dump version 12rc1

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
-- Name: yumebot; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE yumebot WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE yumebot OWNER TO postgres;

\connect yumebot

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    role_id bigint NOT NULL,
    guild_id bigint NOT NULL,
    admin boolean NOT NULL
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: anon; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anon (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.anon OWNER TO postgres;

--
-- Name: anon_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anon_logs (
    message_id bigint NOT NULL,
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.anon_logs OWNER TO postgres;

--
-- Name: anon_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anon_users (
    user_id bigint NOT NULL,
    blocked boolean DEFAULT false NOT NULL,
    guild_id bigint NOT NULL
);


ALTER TABLE public.anon_users OWNER TO postgres;

--
-- Name: blacklist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blacklist (
    user_id bigint NOT NULL,
    reason text NOT NULL,
    "time" timestamp with time zone NOT NULL
);


ALTER TABLE public.blacklist OWNER TO postgres;

--
-- Name: chan_network; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chan_network (
    chan_id bigint NOT NULL,
    guild_id bigint NOT NULL
);


ALTER TABLE public.chan_network OWNER TO postgres;

--
-- Name: guild; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.guild (
    guild_id bigint NOT NULL,
    blacklist boolean NOT NULL,
    color boolean NOT NULL,
    greet boolean NOT NULL,
    greet_chan bigint,
    log_chan bigint,
    logging boolean NOT NULL,
    setup boolean NOT NULL,
    vip boolean NOT NULL
);


ALTER TABLE public.guild OWNER TO postgres;

--
-- Name: muted; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.muted (
    user_id bigint NOT NULL,
    guild_id bigint NOT NULL
);


ALTER TABLE public.muted OWNER TO postgres;

--
-- Name: private; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.private (
    guild_id bigint NOT NULL,
    cat_id bigint NOT NULL,
    role_id bigint NOT NULL,
    name_prefix text DEFAULT 'private'::text NOT NULL,
    hub_id bigint NOT NULL
);


ALTER TABLE public.private OWNER TO postgres;

--
-- Name: private_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.private_users (
    user_id bigint NOT NULL,
    cat_id bigint NOT NULL,
    chan_id bigint NOT NULL
);


ALTER TABLE public.private_users OWNER TO postgres;

--
-- Name: rankings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rankings (
    user_id bigint NOT NULL,
    guild_id bigint NOT NULL,
    level bigint NOT NULL,
    xp bigint NOT NULL,
    total bigint NOT NULL,
    reach bigint NOT NULL
);


ALTER TABLE public.rankings OWNER TO postgres;

--
-- Name: rankings_chan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rankings_chan (
    guild_id bigint NOT NULL,
    chan_id bigint NOT NULL
);


ALTER TABLE public.rankings_chan OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL,
    level bigint NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: sanctions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sanctions (
    sanction_id numeric NOT NULL,
    event text NOT NULL,
    guild_id bigint NOT NULL,
    moderator_id bigint NOT NULL,
    reason text,
    "time" bigint,
    user_id bigint NOT NULL,
    event_date date NOT NULL
);


ALTER TABLE public.sanctions OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    user_id bigint NOT NULL,
    vip boolean NOT NULL,
    crew boolean NOT NULL,
    description text NOT NULL,
    married boolean DEFAULT false NOT NULL,
    lover bigint
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_network; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_network (
    user_id bigint NOT NULL
);


ALTER TABLE public.user_network OWNER TO postgres;

--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (role_id, guild_id);


--
-- Name: anon_users anon_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anon_users
    ADD CONSTRAINT anon_users_pkey PRIMARY KEY (user_id, guild_id);


--
-- Name: muted muted_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.muted
    ADD CONSTRAINT muted_pkey PRIMARY KEY (user_id, guild_id);


--
-- Name: private_users private_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private_users
    ADD CONSTRAINT private_users_pkey PRIMARY KEY (user_id, cat_id);


--
-- Name: rankings rankings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rankings
    ADD CONSTRAINT rankings_pkey PRIMARY KEY (user_id, guild_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (guild_id, level);


--
-- Name: anon unique_anon_guild_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anon
    ADD CONSTRAINT unique_anon_guild_id UNIQUE (guild_id);


--
-- Name: anon_logs unique_anon_logs_message_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anon_logs
    ADD CONSTRAINT unique_anon_logs_message_id UNIQUE (message_id);


--
-- Name: blacklist unique_blacklist_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blacklist
    ADD CONSTRAINT unique_blacklist_user_id PRIMARY KEY (user_id);


--
-- Name: chan_network unique_chan_network_chan_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chan_network
    ADD CONSTRAINT unique_chan_network_chan_id UNIQUE (chan_id);


--
-- Name: guild unique_guild_guild_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guild
    ADD CONSTRAINT unique_guild_guild_id PRIMARY KEY (guild_id);


--
-- Name: private unique_private_cat_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private
    ADD CONSTRAINT unique_private_cat_id PRIMARY KEY (cat_id);


--
-- Name: private unique_private_hub_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private
    ADD CONSTRAINT unique_private_hub_id UNIQUE (hub_id);


--
-- Name: private_users unique_private_users_chan_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private_users
    ADD CONSTRAINT unique_private_users_chan_id UNIQUE (chan_id);


--
-- Name: rankings_chan unique_rankings_chan_chan_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rankings_chan
    ADD CONSTRAINT unique_rankings_chan_chan_id UNIQUE (chan_id);


--
-- Name: sanctions unique_sanctions_sanction_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sanctions
    ADD CONSTRAINT unique_sanctions_sanction_id PRIMARY KEY (sanction_id);


--
-- Name: user unique_user_lover; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT unique_user_lover UNIQUE (lover);


--
-- Name: user_network unique_user_network_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_network
    ADD CONSTRAINT unique_user_network_user_id UNIQUE (user_id);


--
-- Name: user unique_user_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT unique_user_user_id PRIMARY KEY (user_id);


--
-- Name: index_guild_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_guild_id ON public.private USING btree (guild_id);


--
-- PostgreSQL database dump complete
--

