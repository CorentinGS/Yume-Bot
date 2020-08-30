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
    role_id text NOT NULL,
    guild_id text NOT NULL,
    admin boolean NOT NULL
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: anon; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anon (
    guild_id text NOT NULL,
    channel_id text NOT NULL
);


ALTER TABLE public.anon OWNER TO postgres;

--
-- Name: anon_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anon_logs (
    message_id text NOT NULL,
    guild_id text NOT NULL,
    user_id text NOT NULL
);


ALTER TABLE public.anon_logs OWNER TO postgres;

--
-- Name: anon_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anon_users (
    user_id text NOT NULL,
    blocked boolean DEFAULT false NOT NULL,
    guild_id text NOT NULL
);


ALTER TABLE public.anon_users OWNER TO postgres;

--
-- Name: chan_network; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chan_network (
    chan_id text NOT NULL,
    guild_id text NOT NULL
);


ALTER TABLE public.chan_network OWNER TO postgres;

--
-- Name: d_date; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.d_date (
    date_dim_id integer NOT NULL,
    date_actual date NOT NULL,
    epoch bigint NOT NULL,
    day_suffix character varying(4) NOT NULL,
    day_name character varying(9) NOT NULL,
    day_of_week integer NOT NULL,
    day_of_month integer NOT NULL,
    day_of_quarter integer NOT NULL,
    day_of_year integer NOT NULL,
    week_of_month integer NOT NULL,
    week_of_year integer NOT NULL,
    week_of_year_iso character(10) NOT NULL,
    month_actual integer NOT NULL,
    month_name character varying(9) NOT NULL,
    month_name_abbreviated character(3) NOT NULL,
    quarter_actual integer NOT NULL,
    quarter_name character varying(9) NOT NULL,
    year_actual integer NOT NULL,
    first_day_of_week date NOT NULL,
    last_day_of_week date NOT NULL,
    first_day_of_month date NOT NULL,
    last_day_of_month date NOT NULL,
    first_day_of_quarter date NOT NULL,
    last_day_of_quarter date NOT NULL,
    first_day_of_year date NOT NULL,
    last_day_of_year date NOT NULL,
    mmyyyy character(6) NOT NULL,
    mmddyyyy character(10) NOT NULL,
    weekend_indr boolean NOT NULL
);


ALTER TABLE public.d_date OWNER TO postgres;

--
-- Name: daily_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.daily_messages (
    id integer NOT NULL,
    guild_id text NOT NULL,
    date_id integer NOT NULL,
    counter integer NOT NULL
);


ALTER TABLE public.daily_messages OWNER TO postgres;

--
-- Name: daily_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.daily_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.daily_messages_id_seq OWNER TO postgres;

--
-- Name: daily_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.daily_messages_id_seq OWNED BY public.daily_messages.id;


--
-- Name: guild; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.guild (
    guild_id text NOT NULL,
    blacklist boolean NOT NULL,
    color boolean NOT NULL,
    greet boolean NOT NULL,
    greet_chan text,
    log_chan text,
    logging boolean NOT NULL,
    setup boolean NOT NULL,
    vip boolean NOT NULL
);


ALTER TABLE public.guild OWNER TO postgres;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    message_id text NOT NULL,
    guild_id text NOT NULL,
    channel_id text NOT NULL,
    user_id text NOT NULL,
    time_id integer NOT NULL
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: muted; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.muted (
    user_id text NOT NULL,
    guild_id text NOT NULL
);


ALTER TABLE public.muted OWNER TO postgres;

--
-- Name: private; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.private (
    guild_id text NOT NULL,
    cat_id text NOT NULL,
    role_id text NOT NULL,
    name_prefix text DEFAULT 'private'::text NOT NULL,
    hub_id text NOT NULL
);


ALTER TABLE public.private OWNER TO postgres;

--
-- Name: private_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.private_users (
    user_id text NOT NULL,
    cat_id text NOT NULL,
    chan_id text NOT NULL
);


ALTER TABLE public.private_users OWNER TO postgres;

--
-- Name: rankings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rankings (
    user_id text NOT NULL,
    guild_id text NOT NULL,
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
    guild_id text NOT NULL,
    chan_id text NOT NULL
);


ALTER TABLE public.rankings_chan OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    guild_id text NOT NULL,
    role_id text NOT NULL,
    level integer NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: sanctions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sanctions (
    sanction_id text NOT NULL,
    event text NOT NULL,
    guild_id text NOT NULL,
    moderator_id text NOT NULL,
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
    user_id text NOT NULL,
    vip boolean NOT NULL,
    crew boolean NOT NULL,
    description text NOT NULL,
    married boolean DEFAULT false NOT NULL,
    lover text
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_network; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_network (
    user_id text NOT NULL
);


ALTER TABLE public.user_network OWNER TO postgres;

--
-- Name: daily_messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_messages ALTER COLUMN id SET DEFAULT nextval('public.daily_messages_id_seq'::regclass);


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
-- Name: d_date d_date_date_dim_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.d_date
    ADD CONSTRAINT d_date_date_dim_id_pk PRIMARY KEY (date_dim_id);


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
-- Name: messages unique_messages_message_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT unique_messages_message_id UNIQUE (message_id);


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
-- Name: d_date_date_actual_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX d_date_date_actual_idx ON public.d_date USING btree (date_actual);


--
-- Name: index_guild_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_guild_id ON public.private USING btree (guild_id);


--
-- PostgreSQL database dump complete
--

