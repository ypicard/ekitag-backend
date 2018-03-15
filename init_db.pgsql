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
    password TEXT,
    gold_stars INTEGER DEFAULT 0,
    silver_stars INTEGER DEFAULT 0,
    bronze_stars INTEGER DEFAULT 0,
    loser_stars INTEGER DEFAULT 0
);

-- MATCHES
CREATE TABLE matches (
 id serial PRIMARY KEY,
 b1_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 b2_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 b3_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 b4_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 b5_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 b6_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r1_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r2_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r3_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r4_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r5_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r6_id INTEGER REFERENCES users(id) ON DELETE RESTRICT,
 r_score INTEGER NOT NULL,
 b_score INTEGER NOT NULL,
 duration INTERVAL NOT NULL,
 validated_by INTEGER REFERENCES users(id),
 datetime TIMESTAMP WITH TIME ZONE NOT NULL
);

-- PENDING MATCHES
CREATE TABLE matches_pending (
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
 duration INTERVAL NOT NULL,
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
    season_id INTEGER REFERENCES seasons(id) ON DELETE CASCADE,
    match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
    UNIQUE (season_id, match_id)
);

-- STATISTICS
CREATE TABLE statistics (
    id serial PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
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
    pups INTEGER,
    UNIQUE (match_id, user_id)
);

-- STATISTICS_PENDING
CREATE TABLE statistics_pending (
    id serial PRIMARY KEY,
    match_id INTEGER REFERENCES matches_pending(id) ON DELETE CASCADE,
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
    pups INTEGER,
    UNIQUE(match_id, user_pseudo)
);

-- MUSIGMA TEAM
CREATE TABLE musigma_team (
    id serial PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    season_id INTEGER REFERENCES seasons(id) ON DELETE CASCADE,
    match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
    exposition DECIMAL NOT NULL,
    mu DECIMAL NOT NULL,
    sigma DECIMAL NOT NULL,
    UNIQUE (user_id, season_id, match_id)
);

-- TO ALLOW ONLY ONE (USER_ID, NULL_SEASON_ID) ROW: PARTIAL INDEX
CREATE UNIQUE INDEX musigma_team_global_uni_idx ON musigma_team (user_id, match_id)
WHERE season_id IS NULL;

-- POPULATE ADMINS
INSERT INTO users (trigram, pseudo, is_admin, password) VALUES ('yap', 'Yapus', true, crypt('107410', gen_salt('bf')));
INSERT INTO users (trigram, pseudo, is_admin, password) VALUES ('frm', 'Covfefe', true, crypt('107410', gen_salt('bf')));
INSERT INTO users (trigram, pseudo, is_admin, password) VALUES ('vis', 'cousinVic', true, crypt('107410', gen_salt('bf')));

-- POPULATE OTHERS
INSERT INTO users (trigram, pseudo) VALUES ('pim', 'Pro');
INSERT INTO users (trigram, pseudo) VALUES ('mav', 'Maxou');
INSERT INTO users (trigram, pseudo) VALUES ('yob', 'Roxxor');
INSERT INTO users (trigram, pseudo) VALUES ('gub', 'SuperSouyon');
INSERT INTO users (trigram, pseudo) VALUES ('bar', 'Tente');
INSERT INTO users (trigram, pseudo) VALUES ('iss', 'Ekisomox');
INSERT INTO users (trigram, pseudo) VALUES ('sal', 'Ticket Resto');
INSERT INTO users (trigram, pseudo) VALUES ('mad', 'Fonky');
INSERT INTO users (trigram, pseudo) VALUES ('clb', 'DataArtist');
INSERT INTO users (trigram, pseudo) VALUES ('jec', 'The Bouboule');
INSERT INTO users (trigram, pseudo) VALUES ('wat', 'JiSK');
INSERT INTO users (trigram, pseudo) VALUES ('baa', 'Batamanq');
INSERT INTO users (trigram, pseudo) VALUES ('abd', 'Nulos');
INSERT INTO users (trigram, pseudo) VALUES ('cea', 'Moules');
INSERT INTO users (trigram, pseudo) VALUES ('hes', 'Ancestro');
INSERT INTO users (trigram, pseudo) VALUES ('arf', 'Bogoss');
