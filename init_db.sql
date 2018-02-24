DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE EXTENSION pgcrypto;
-- USERS
CREATE TABLE users (
    id serial PRIMARY KEY,
    trigram VARCHAR(3) UNIQUE,
    pseudo VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    usual_pseudos VARCHAR(50)[],
    is_admin BOOLEAN DEFAULT false,
    password TEXT NOT NULL,
    gold_stars INTEGER DEFAULT 0,
    silver_stars INTEGER DEFAULT 0,
    copper_stars INTEGER DEFAULT 0,
    loser_stars INTEGER DEFAULT 0
);

-- MATCHES
CREATE TABLE matches (
 id serial PRIMARY KEY,
 b1_id INTEGER REFERENCES users(id) NOT NULL,
 b2_id INTEGER REFERENCES users(id),
 b3_id INTEGER REFERENCES users(id),
 b4_id INTEGER REFERENCES users(id),
 b5_id INTEGER REFERENCES users(id),
 b6_id INTEGER REFERENCES users(id),
 r1_id INTEGER REFERENCES users(id) NOT NULL,
 r2_id INTEGER REFERENCES users(id),
 r3_id INTEGER REFERENCES users(id),
 r4_id INTEGER REFERENCES users(id),
 r5_id INTEGER REFERENCES users(id),
 r6_id INTEGER REFERENCES users(id),
 r_score INTEGER NOT NULL,
 b_score INTEGER NOT NULL,
 validated_by INTEGER REFERENCES users(id),
 datetime TIMESTAMP WITH TIME ZONE NOT NULL
);

-- PENDING MATCHES
CREATE TABLE pending_matches (
 id serial PRIMARY KEY,
 b1_pseudo VARCHAR(50) NOT NULL,
 b2_pseudo VARCHAR(50),
 b3_pseudo VARCHAR(50),
 b4_pseudo VARCHAR(50),
 b5_pseudo VARCHAR(50),
 b6_pseudo VARCHAR(50),
 r1_pseudo VARCHAR(50) NOT NULL,
 r2_pseudo VARCHAR(50),
 r3_pseudo VARCHAR(50),
 r4_pseudo VARCHAR(50),
 r5_pseudo VARCHAR(50),
 r6_pseudo VARCHAR(50),
 r_score INTEGER NOT NULL,
 b_score INTEGER NOT NULL,
 datetime TIMESTAMP WITH TIME ZONE NOT NULL
);

-- SEASONS
CREATE TABLE seasons (
    id serial PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    end_time TIMESTAMP WITH TIME ZONE,
    max_time INTERVAL,
    max_matches INTEGER,
    running BOOLEAN DEFAULT true,
    played_matches INTEGER DEFAULT 0
);

-- SEASONS_MATCHES
CREATE TABLE seasons_matches (
    id serial PRIMARY KEY,
    season_id INTEGER REFERENCES seasons(id),
    match_id INTEGER REFERENCES matches(id)
);

-- STATISTICS
CREATE TABLE statistics (
    id serial PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    score INTEGER,
    tags INTEGER,
    popped INTEGER,
    grabs INTEGER,
    drops INTEGER,
    hold INTERVAL,
    captures INTEGER,
    prevent  INTERVAL,
    returns INTEGER,
    support INTEGER,
    pups INTEGER
);

-- STATISTICS_PENDING
CREATE TABLE statistics_pending (
    id serial PRIMARY KEY,
    match_id INTEGER REFERENCES pending_matches(id) ON DELETE CASCADE,
    user_pseudo VARCHAR(50) NOT NULL,
    score INTEGER,
    tags INTEGER,
    popped INTEGER,
    grabs INTEGER,
    drops INTEGER,
    hold INTERVAL,
    captures INTEGER,
    prevent INTERVAL,
    returns INTEGER,
    support INTEGER,
    pups INTEGER
);

-- MUSIGMA TEAM GLOBAL
CREATE TABLE musigma_team_global (
    id serial PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    mu DECIMAL NOT NULL,
    sigma DECIMAL NOT NULL
);

-- POPULATE
INSERT INTO users (trigram, pseudo, is_admin, password) VALUES ('yap', 'Yapus', true, crypt('107410', gen_salt('bf')));