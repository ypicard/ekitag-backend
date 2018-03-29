--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 10.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: matches; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE matches (
    id integer NOT NULL,
    b1_id integer,
    b2_id integer,
    b3_id integer,
    b4_id integer,
    b5_id integer,
    b6_id integer,
    r1_id integer,
    r2_id integer,
    r3_id integer,
    r4_id integer,
    r5_id integer,
    r6_id integer,
    r_score integer NOT NULL,
    b_score integer NOT NULL,
    duration interval NOT NULL,
    validated_by integer,
    datetime timestamp with time zone NOT NULL
);


ALTER TABLE matches OWNER TO rklvuyqrechuta;

--
-- Name: matches_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE matches_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE matches_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: matches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE matches_id_seq OWNED BY matches.id;


--
-- Name: matches_pending; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE matches_pending (
    id integer NOT NULL,
    b1_pseudo character varying(50) NOT NULL,
    b2_pseudo character varying(50),
    b3_pseudo character varying(50),
    b4_pseudo character varying(50),
    b5_pseudo character varying(50),
    b6_pseudo character varying(50),
    r1_pseudo character varying(50) NOT NULL,
    r2_pseudo character varying(50),
    r3_pseudo character varying(50),
    r4_pseudo character varying(50),
    r5_pseudo character varying(50),
    r6_pseudo character varying(50),
    r_score integer NOT NULL,
    b_score integer NOT NULL,
    duration interval NOT NULL,
    datetime timestamp with time zone NOT NULL
);


ALTER TABLE matches_pending OWNER TO rklvuyqrechuta;

--
-- Name: matches_pending_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE matches_pending_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE matches_pending_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: matches_pending_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE matches_pending_id_seq OWNED BY matches_pending.id;


--
-- Name: musigma_team; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE musigma_team (
    id integer NOT NULL,
    user_id integer,
    season_id integer,
    match_id integer,
    exposition numeric NOT NULL,
    mu numeric NOT NULL,
    sigma numeric NOT NULL
);


ALTER TABLE musigma_team OWNER TO rklvuyqrechuta;

--
-- Name: musigma_team_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE musigma_team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE musigma_team_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: musigma_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE musigma_team_id_seq OWNED BY musigma_team.id;


--
-- Name: seasons; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE seasons (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    start_time timestamp with time zone DEFAULT now() NOT NULL,
    end_time timestamp with time zone,
    max_time interval,
    max_matches integer,
    running boolean DEFAULT true,
    played_matches integer DEFAULT 0
);


ALTER TABLE seasons OWNER TO rklvuyqrechuta;

--
-- Name: seasons_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE seasons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE seasons_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: seasons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE seasons_id_seq OWNED BY seasons.id;


--
-- Name: seasons_matches; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE seasons_matches (
    id integer NOT NULL,
    season_id integer,
    match_id integer
);


ALTER TABLE seasons_matches OWNER TO rklvuyqrechuta;

--
-- Name: seasons_matches_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE seasons_matches_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE seasons_matches_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: seasons_matches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE seasons_matches_id_seq OWNED BY seasons_matches.id;


--
-- Name: statistics; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE statistics (
    id integer NOT NULL,
    match_id integer,
    user_id integer,
    score integer,
    tags integer,
    popped integer,
    grabs integer,
    drops integer,
    hold interval,
    captures integer,
    prevent interval,
    returns integer,
    support integer,
    pups integer
);


ALTER TABLE statistics OWNER TO rklvuyqrechuta;

--
-- Name: statistics_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE statistics_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statistics_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: statistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE statistics_id_seq OWNED BY statistics.id;


--
-- Name: statistics_pending; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE statistics_pending (
    id integer NOT NULL,
    match_id integer,
    user_pseudo character varying(50) NOT NULL,
    score integer,
    tags integer,
    popped integer,
    grabs integer,
    drops integer,
    hold interval,
    captures integer,
    prevent interval,
    returns integer,
    support integer,
    pups integer
);


ALTER TABLE statistics_pending OWNER TO rklvuyqrechuta;

--
-- Name: statistics_pending_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE statistics_pending_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE statistics_pending_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: statistics_pending_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE statistics_pending_id_seq OWNED BY statistics_pending.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: rklvuyqrechuta
--

CREATE TABLE users (
    id integer NOT NULL,
    trigram character varying(3),
    pseudo character varying(50),
    is_active boolean DEFAULT true,
    usual_pseudos character varying(50)[],
    is_admin boolean DEFAULT false,
    password text,
    gold_stars integer DEFAULT 0,
    silver_stars integer DEFAULT 0,
    bronze_stars integer DEFAULT 0,
    loser_stars integer DEFAULT 0
);


ALTER TABLE users OWNER TO rklvuyqrechuta;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: rklvuyqrechuta
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO rklvuyqrechuta;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rklvuyqrechuta
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: matches id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches ALTER COLUMN id SET DEFAULT nextval('matches_id_seq'::regclass);


--
-- Name: matches_pending id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches_pending ALTER COLUMN id SET DEFAULT nextval('matches_pending_id_seq'::regclass);


--
-- Name: musigma_team id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY musigma_team ALTER COLUMN id SET DEFAULT nextval('musigma_team_id_seq'::regclass);


--
-- Name: seasons id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons ALTER COLUMN id SET DEFAULT nextval('seasons_id_seq'::regclass);


--
-- Name: seasons_matches id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons_matches ALTER COLUMN id SET DEFAULT nextval('seasons_matches_id_seq'::regclass);


--
-- Name: statistics id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics ALTER COLUMN id SET DEFAULT nextval('statistics_id_seq'::regclass);


--
-- Name: statistics_pending id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics_pending ALTER COLUMN id SET DEFAULT nextval('statistics_pending_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: matches; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY matches (id, b1_id, b2_id, b3_id, b4_id, b5_id, b6_id, r1_id, r2_id, r3_id, r4_id, r5_id, r6_id, r_score, b_score, duration, validated_by, datetime) FROM stdin;
\.


--
-- Data for Name: matches_pending; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY matches_pending (id, b1_pseudo, b2_pseudo, b3_pseudo, b4_pseudo, b5_pseudo, b6_pseudo, r1_pseudo, r2_pseudo, r3_pseudo, r4_pseudo, r5_pseudo, r6_pseudo, r_score, b_score, duration, datetime) FROM stdin;
1	SIGKILL	420	----)	Tommy Tomato	null	null	Some Ball 4	Kamiko	king dedede	ItsmeBeyonce	null	null	2	3	00:10:00	2018-03-15 10:55:58.724+00
5	El-Soyador	\N	\N	\N	\N	\N	Bite en boite	\N	\N	\N	\N	\N	5	3	00:10:00	2018-03-16 16:00:58.087041+00
\.


--
-- Data for Name: musigma_team; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY musigma_team (id, user_id, season_id, match_id, exposition, mu, sigma) FROM stdin;
\.


--
-- Data for Name: seasons; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY seasons (id, name, start_time, end_time, max_time, max_matches, running, played_matches) FROM stdin;
\.


--
-- Data for Name: seasons_matches; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY seasons_matches (id, season_id, match_id) FROM stdin;
\.


--
-- Data for Name: statistics; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY statistics (id, match_id, user_id, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups) FROM stdin;
\.


--
-- Data for Name: statistics_pending; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY statistics_pending (id, match_id, user_pseudo, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups) FROM stdin;
1	1	Some Ball 4	54	9	7	6	5	00:01:11	1	00:00:37	8	13	4
2	1	----)	34	5	5	4	3	00:00:37	1	00:00:32	5	3	2
3	1	Kamiko	35	10	10	6	5	00:00:32	1	00:00:16	3	10	3
4	1	420	36	7	12	7	7	00:01:08	0	00:00:06	5	16	7
5	1	SIGKILL	40	9	9	6	5	00:00:29	1	00:00:41	3	13	3
6	1	king dedede	28	2	13	7	7	00:01:31	0	00:00:31	2	12	5
7	1	Tommy Tomato	25	3	4	4	3	00:00:42	1	00:00:06	3	4	1
8	1	ItsmeBeyonce	2	1	4	2	2	00:00:03	0	00:00:06	1	2	0
9	5	El-Soyador	5	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
10	5	Bite en boite	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: rklvuyqrechuta
--

COPY users (id, trigram, pseudo, is_active, usual_pseudos, is_admin, password, gold_stars, silver_stars, bronze_stars, loser_stars) FROM stdin;
1	yap	Yapus	t	\N	t	$2a$06$8XU/WbXxkvSdAGQJa3FA1eFP/QF9mUDoAUfUAYcDmly8mv1GtIM0.	0	0	0	0
2	frm	Covfefe	t	\N	t	$2a$06$DCmNZADG2GOmHPK0oBxTDuPd2Q/kx55HbM5MXK5KFo66tpvVqH3hq	0	0	0	0
3	vis	cousinVic	t	\N	t	$2a$06$CiTQfjHvYc43zMerqHHUT.mvfKujFToaViB.xgXZ.Ed3sZUv3G9Oa	0	0	0	0
4	pim	Pro	t	\N	f	\N	0	0	0	0
5	mav	Maxou	t	\N	f	\N	0	0	0	0
6	yob	Roxxor	t	\N	f	\N	0	0	0	0
8	bar	Tente	t	\N	f	\N	0	0	0	0
9	iss	Ekisomox	t	\N	f	\N	0	0	0	0
10	sal	Ticket Resto	t	\N	f	\N	0	0	0	0
11	mad	Fonky	t	\N	f	\N	0	0	0	0
12	clb	DataArtist	t	\N	f	\N	0	0	0	0
13	jec	The Bouboule	t	\N	f	\N	0	0	0	0
14	wat	JiSK	t	\N	f	\N	0	0	0	0
15	baa	Batamanq	t	\N	f	\N	0	0	0	0
16	abd	Nulos	t	\N	f	\N	0	0	0	0
17	cea	Moules	t	\N	f	\N	0	0	0	0
19	arf	Bogoss	t	\N	f	\N	0	0	0	0
18	hes	Ancestro	t	{"Bite en boite"}	f	\N	0	0	0	0
7	gub	Souillon	t	{El-Soyador,Bite,"Double Bite"}	f	\N	0	0	0	0
\.


--
-- Name: matches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('matches_id_seq', 1, true);


--
-- Name: matches_pending_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('matches_pending_id_seq', 5, true);


--
-- Name: musigma_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('musigma_team_id_seq', 1, false);


--
-- Name: seasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('seasons_id_seq', 1, false);


--
-- Name: seasons_matches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('seasons_matches_id_seq', 1, false);


--
-- Name: statistics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('statistics_id_seq', 1, false);


--
-- Name: statistics_pending_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('statistics_pending_id_seq', 10, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rklvuyqrechuta
--

SELECT pg_catalog.setval('users_id_seq', 19, true);


--
-- Name: matches_pending matches_pending_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches_pending
    ADD CONSTRAINT matches_pending_pkey PRIMARY KEY (id);


--
-- Name: matches matches_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_pkey PRIMARY KEY (id);


--
-- Name: musigma_team musigma_team_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY musigma_team
    ADD CONSTRAINT musigma_team_pkey PRIMARY KEY (id);


--
-- Name: musigma_team musigma_team_user_id_season_id_match_id_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY musigma_team
    ADD CONSTRAINT musigma_team_user_id_season_id_match_id_key UNIQUE (user_id, season_id, match_id);


--
-- Name: seasons_matches seasons_matches_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons_matches
    ADD CONSTRAINT seasons_matches_pkey PRIMARY KEY (id);


--
-- Name: seasons_matches seasons_matches_season_id_match_id_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons_matches
    ADD CONSTRAINT seasons_matches_season_id_match_id_key UNIQUE (season_id, match_id);


--
-- Name: seasons seasons_name_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons
    ADD CONSTRAINT seasons_name_key UNIQUE (name);


--
-- Name: seasons seasons_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons
    ADD CONSTRAINT seasons_pkey PRIMARY KEY (id);


--
-- Name: statistics statistics_match_id_user_id_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics
    ADD CONSTRAINT statistics_match_id_user_id_key UNIQUE (match_id, user_id);


--
-- Name: statistics_pending statistics_pending_match_id_user_pseudo_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics_pending
    ADD CONSTRAINT statistics_pending_match_id_user_pseudo_key UNIQUE (match_id, user_pseudo);


--
-- Name: statistics_pending statistics_pending_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics_pending
    ADD CONSTRAINT statistics_pending_pkey PRIMARY KEY (id);


--
-- Name: statistics statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics
    ADD CONSTRAINT statistics_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_pseudo_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pseudo_key UNIQUE (pseudo);


--
-- Name: users users_trigram_key; Type: CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_trigram_key UNIQUE (trigram);


--
-- Name: musigma_team_global_uni_idx; Type: INDEX; Schema: public; Owner: rklvuyqrechuta
--

CREATE UNIQUE INDEX musigma_team_global_uni_idx ON musigma_team USING btree (user_id, match_id) WHERE (season_id IS NULL);


--
-- Name: matches matches_b1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_b1_id_fkey FOREIGN KEY (b1_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_b2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_b2_id_fkey FOREIGN KEY (b2_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_b3_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_b3_id_fkey FOREIGN KEY (b3_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_b4_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_b4_id_fkey FOREIGN KEY (b4_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_b5_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_b5_id_fkey FOREIGN KEY (b5_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_b6_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_b6_id_fkey FOREIGN KEY (b6_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_r1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_r1_id_fkey FOREIGN KEY (r1_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_r2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_r2_id_fkey FOREIGN KEY (r2_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_r3_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_r3_id_fkey FOREIGN KEY (r3_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_r4_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_r4_id_fkey FOREIGN KEY (r4_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_r5_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_r5_id_fkey FOREIGN KEY (r5_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_r6_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_r6_id_fkey FOREIGN KEY (r6_id) REFERENCES users(id) ON DELETE RESTRICT;


--
-- Name: matches matches_validated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_validated_by_fkey FOREIGN KEY (validated_by) REFERENCES users(id);


--
-- Name: musigma_team musigma_team_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY musigma_team
    ADD CONSTRAINT musigma_team_match_id_fkey FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE;


--
-- Name: musigma_team musigma_team_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY musigma_team
    ADD CONSTRAINT musigma_team_season_id_fkey FOREIGN KEY (season_id) REFERENCES seasons(id) ON DELETE CASCADE;


--
-- Name: musigma_team musigma_team_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY musigma_team
    ADD CONSTRAINT musigma_team_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: seasons_matches seasons_matches_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons_matches
    ADD CONSTRAINT seasons_matches_match_id_fkey FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE;


--
-- Name: seasons_matches seasons_matches_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY seasons_matches
    ADD CONSTRAINT seasons_matches_season_id_fkey FOREIGN KEY (season_id) REFERENCES seasons(id) ON DELETE CASCADE;


--
-- Name: statistics statistics_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics
    ADD CONSTRAINT statistics_match_id_fkey FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE;


--
-- Name: statistics_pending statistics_pending_match_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics_pending
    ADD CONSTRAINT statistics_pending_match_id_fkey FOREIGN KEY (match_id) REFERENCES matches_pending(id) ON DELETE CASCADE;


--
-- Name: statistics statistics_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rklvuyqrechuta
--

ALTER TABLE ONLY statistics
    ADD CONSTRAINT statistics_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO rklvuyqrechuta;


--
-- PostgreSQL database dump complete
--

