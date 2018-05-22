# -*- coding: utf-8 -*-
# You wish ! ORM are for pussies.

import config
import postgresql
import postgresql.exceptions
import postgresql.types

secret = config.secret()
db = postgresql.open(secret.get('pg_uri'))
transaction = db.xact

# ========================= SQL COMMANDS
# You can ask for any existing field, unused fields will be filtered out using view models.
# If you need to join, always specify AS and mangle names with $.

# ------------------------- USERS
create_user = db.prepare("INSERT INTO users (trigram, pseudo) VALUES ($1, $2) RETURNING id")
get_users = db.prepare("SELECT id, pseudo, usual_pseudos, is_active, gold_stars, silver_stars, bronze_stars, loser_stars FROM users")
update_user = db.prepare("UPDATE users SET pseudo = $2, usual_pseudos = $3 WHERE id = $1")
get_user_by_id = db.prepare("SELECT * FROM users WHERE id = $1 LIMIT 1")
get_user_by_trigram = db.prepare("SELECT * FROM users WHERE trigram = $1 LIMIT 1")
desactivate_user = db.prepare("UPDATE users SET is_active = false WHERE id = $1")
get_user_by_pseudo = db.prepare("SELECT * FROM USERS WHERE $1 = ANY(USUAL_PSEUDOS) OR PSEUDO = $1;")
award_gold_star = db.prepare("UPDATE users SET gold_stars = gold_stars + 1 WHERE id = $1 RETURNING gold_stars")
award_silver_star = db.prepare("UPDATE users SET silver_stars = silver_stars + 1 WHERE id = $1 RETURNING silver_stars")
award_copper_star = db.prepare("UPDATE users SET bronze_stars = bronze_stars + 1 WHERE id = $1 RETURNING bronze_stars")
award_loser_star = db.prepare("UPDATE users SET loser_stars = loser_stars + 1 WHERE id = $1 RETURNING loser_stars")

# ------------------------- ADMIN
promote_user = db.prepare("UPDATE users SET is_admin = true, password = crypt($2, gen_salt('bf')) WHERE id = $1")
auth_admin = db.prepare("SELECT password = crypt($2, password) FROM users WHERE trigram = $1 AND is_admin = true")
block_admin = db.prepare("UPDATE users SET is_admin = false WHERE id = $1")

# ------------------------- MATCHES
create_match = db.prepare(
    "INSERT INTO matches (b_score, r_score, duration, datetime, "
    "b1_id, b2_id, b3_id, b4_id, b5_id, b6_id, "
    "r1_id, r2_id, r3_id, r4_id, r5_id, r6_id, "
    "validated_by) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17) "
    "RETURNING id")
get_matches = db.prepare(
    "SELECT matches.id AS id,  matches.r_score, matches.b_score, matches.duration, matches.datetime,"
    "matches.b1_id, matches.b2_id, matches.b3_id, matches.b4_id, matches.b5_id, matches.b6_id, "
    "matches.r1_id, matches.r2_id, matches.r3_id, matches.r4_id, matches.r5_id, matches.r6_id,"
    "validator.id as validator$id, validator.pseudo as validator$pseudo, validator.usual_pseudos as validator$usual_pseudos, "
    "season.id as season$id, season.name as season$name "
    "FROM matches "
    "LEFT JOIN users AS validator "
    "ON validated_by = validator.id "
    "LEFT JOIN seasons_matches "
    "ON matches.id = seasons_matches.match_id "
    "LEFT JOIN seasons AS season "
    "ON season.id = seasons_matches.season_id "
    "ORDER BY id DESC")
get_match_by_id = db.prepare(
    "SELECT matches.id as id, r_score, b_score, duration, datetime,  "
    "r1.id as r1$id, r1.pseudo as r1$pseudo, "
    "r2.id as r2$id, r2.pseudo as r2$pseudo, "
    "r3.id as r3$id, r3.pseudo as r3$pseudo, "
    "r4.id as r4$id, r4.pseudo as r4$pseudo, "
    "r5.id as r5$id, r5.pseudo as r5$pseudo, "
    "r6.id as r6$id, r6.pseudo as r6$pseudo, "
    "b1.id as b1$id, b1.pseudo as b1$pseudo, "
    "b2.id as b2$id, b2.pseudo as b2$pseudo, "
    "b3.id as b3$id, b3.pseudo as b3$pseudo, "
    "b4.id as b4$id, b4.pseudo as b4$pseudo, "
    "b5.id as b5$id, b5.pseudo as b5$pseudo, "
    "b6.id as b6$id, b6.pseudo as b6$pseudo, "

    "r1_stats.id as r1_stats$id, r1_stats.user_id as r1_stats$user_id, r1_stats.score as r1_stats$score, r1_stats.tags as r1_stats$tags, r1_stats.popped as r1_stats$popped, r1_stats.grabs as r1_stats$grabs, r1_stats.drops as r1_stats$drops, r1_stats.hold as r1_stats$hold, r1_stats.captures as r1_stats$captures, r1_stats.prevent as r1_stats$prevent, r1_stats.returns as r1_stats$returns, r1_stats.support as r1_stats$support, r1_stats.pups as r1_stats$pups, "
    "r2_stats.id as r2_stats$id, r2_stats.user_id as r2_stats$user_id, r2_stats.score as r2_stats$score, r2_stats.tags as r2_stats$tags, r2_stats.popped as r2_stats$popped, r2_stats.grabs as r2_stats$grabs, r2_stats.drops as r2_stats$drops, r2_stats.hold as r2_stats$hold, r2_stats.captures as r2_stats$captures, r2_stats.prevent as r2_stats$prevent, r2_stats.returns as r2_stats$returns, r2_stats.support as r2_stats$support, r2_stats.pups as r2_stats$pups, "
    "r3_stats.id as r3_stats$id, r3_stats.user_id as r3_stats$user_id, r3_stats.score as r3_stats$score, r3_stats.tags as r3_stats$tags, r3_stats.popped as r3_stats$popped, r3_stats.grabs as r3_stats$grabs, r3_stats.drops as r3_stats$drops, r3_stats.hold as r3_stats$hold, r3_stats.captures as r3_stats$captures, r3_stats.prevent as r3_stats$prevent, r3_stats.returns as r3_stats$returns, r3_stats.support as r3_stats$support, r3_stats.pups as r3_stats$pups, "
    "r4_stats.id as r4_stats$id, r4_stats.user_id as r4_stats$user_id, r4_stats.score as r4_stats$score, r4_stats.tags as r4_stats$tags, r4_stats.popped as r4_stats$popped, r4_stats.grabs as r4_stats$grabs, r4_stats.drops as r4_stats$drops, r4_stats.hold as r4_stats$hold, r4_stats.captures as r4_stats$captures, r4_stats.prevent as r4_stats$prevent, r4_stats.returns as r4_stats$returns, r4_stats.support as r4_stats$support, r4_stats.pups as r4_stats$pups, "
    "r5_stats.id as r5_stats$id, r5_stats.user_id as r5_stats$user_id, r5_stats.score as r5_stats$score, r5_stats.tags as r5_stats$tags, r5_stats.popped as r5_stats$popped, r5_stats.grabs as r5_stats$grabs, r5_stats.drops as r5_stats$drops, r5_stats.hold as r5_stats$hold, r5_stats.captures as r5_stats$captures, r5_stats.prevent as r5_stats$prevent, r5_stats.returns as r5_stats$returns, r5_stats.support as r5_stats$support, r5_stats.pups as r5_stats$pups, "
    "r6_stats.id as r6_stats$id, r6_stats.user_id as r6_stats$user_id, r6_stats.score as r6_stats$score, r6_stats.tags as r6_stats$tags, r6_stats.popped as r6_stats$popped, r6_stats.grabs as r6_stats$grabs, r6_stats.drops as r6_stats$drops, r6_stats.hold as r6_stats$hold, r6_stats.captures as r6_stats$captures, r6_stats.prevent as r6_stats$prevent, r6_stats.returns as r6_stats$returns, r6_stats.support as r6_stats$support, r6_stats.pups as r6_stats$pups, "
    "b1_stats.id as b1_stats$id, b1_stats.user_id as b1_stats$user_id, b1_stats.score as b1_stats$score, b1_stats.tags as b1_stats$tags, b1_stats.popped as b1_stats$popped, b1_stats.grabs as b1_stats$grabs, b1_stats.drops as b1_stats$drops, b1_stats.hold as b1_stats$hold, b1_stats.captures as b1_stats$captures, b1_stats.prevent as b1_stats$prevent, b1_stats.returns as b1_stats$returns, b1_stats.support as b1_stats$support, b1_stats.pups as b1_stats$pups, "
    "b2_stats.id as b2_stats$id, b2_stats.user_id as b2_stats$user_id, b2_stats.score as b2_stats$score, b2_stats.tags as b2_stats$tags, b2_stats.popped as b2_stats$popped, b2_stats.grabs as b2_stats$grabs, b2_stats.drops as b2_stats$drops, b2_stats.hold as b2_stats$hold, b2_stats.captures as b2_stats$captures, b2_stats.prevent as b2_stats$prevent, b2_stats.returns as b2_stats$returns, b2_stats.support as b2_stats$support, b2_stats.pups as b2_stats$pups, "
    "b3_stats.id as b3_stats$id, b3_stats.user_id as b3_stats$user_id, b3_stats.score as b3_stats$score, b3_stats.tags as b3_stats$tags, b3_stats.popped as b3_stats$popped, b3_stats.grabs as b3_stats$grabs, b3_stats.drops as b3_stats$drops, b3_stats.hold as b3_stats$hold, b3_stats.captures as b3_stats$captures, b3_stats.prevent as b3_stats$prevent, b3_stats.returns as b3_stats$returns, b3_stats.support as b3_stats$support, b3_stats.pups as b3_stats$pups, "
    "b4_stats.id as b4_stats$id, b4_stats.user_id as b4_stats$user_id, b4_stats.score as b4_stats$score, b4_stats.tags as b4_stats$tags, b4_stats.popped as b4_stats$popped, b4_stats.grabs as b4_stats$grabs, b4_stats.drops as b4_stats$drops, b4_stats.hold as b4_stats$hold, b4_stats.captures as b4_stats$captures, b4_stats.prevent as b4_stats$prevent, b4_stats.returns as b4_stats$returns, b4_stats.support as b4_stats$support, b4_stats.pups as b4_stats$pups, "
    "b5_stats.id as b5_stats$id, b5_stats.user_id as b5_stats$user_id, b5_stats.score as b5_stats$score, b5_stats.tags as b5_stats$tags, b5_stats.popped as b5_stats$popped, b5_stats.grabs as b5_stats$grabs, b5_stats.drops as b5_stats$drops, b5_stats.hold as b5_stats$hold, b5_stats.captures as b5_stats$captures, b5_stats.prevent as b5_stats$prevent, b5_stats.returns as b5_stats$returns, b5_stats.support as b5_stats$support, b5_stats.pups as b5_stats$pups, "
    "b6_stats.id as b6_stats$id, b6_stats.user_id as b6_stats$user_id, b6_stats.score as b6_stats$score, b6_stats.tags as b6_stats$tags, b6_stats.popped as b6_stats$popped, b6_stats.grabs as b6_stats$grabs, b6_stats.drops as b6_stats$drops, b6_stats.hold as b6_stats$hold, b6_stats.captures as b6_stats$captures, b6_stats.prevent as b6_stats$prevent, b6_stats.returns as b6_stats$returns, b6_stats.support as b6_stats$support, b6_stats.pups as b6_stats$pups, "

    "validator.id as validator$id, validator.pseudo as validator$pseudo, "
    "season.id as season$id, season.name as season$name "
    "FROM matches  "

    "LEFT JOIN users AS validator ON validated_by = validator.id "

    "LEFT JOIN statistics AS r1_stats ON r1_stats.match_id = matches.id AND r1_stats.user_id = matches.r1_id "
    "LEFT JOIN statistics AS r2_stats ON r2_stats.match_id = matches.id AND r2_stats.user_id = matches.r2_id "
    "LEFT JOIN statistics AS r3_stats ON r3_stats.match_id = matches.id AND r3_stats.user_id = matches.r3_id "
    "LEFT JOIN statistics AS r4_stats ON r4_stats.match_id = matches.id AND r4_stats.user_id = matches.r4_id "
    "LEFT JOIN statistics AS r5_stats ON r5_stats.match_id = matches.id AND r5_stats.user_id = matches.r5_id "
    "LEFT JOIN statistics AS r6_stats ON r6_stats.match_id = matches.id AND r6_stats.user_id = matches.r6_id "
    "LEFT JOIN statistics AS b1_stats ON b1_stats.match_id = matches.id AND b1_stats.user_id = matches.b1_id "
    "LEFT JOIN statistics AS b2_stats ON b2_stats.match_id = matches.id AND b2_stats.user_id = matches.b2_id "
    "LEFT JOIN statistics AS b3_stats ON b3_stats.match_id = matches.id AND b3_stats.user_id = matches.b3_id "
    "LEFT JOIN statistics AS b4_stats ON b4_stats.match_id = matches.id AND b4_stats.user_id = matches.b4_id "
    "LEFT JOIN statistics AS b5_stats ON b5_stats.match_id = matches.id AND b5_stats.user_id = matches.b5_id "
    "LEFT JOIN statistics AS b6_stats ON b6_stats.match_id = matches.id AND b6_stats.user_id = matches.b6_id "

    "LEFT JOIN users AS r1 ON r1.id = matches.r1_id "
    "LEFT JOIN users AS r2 ON r2.id = matches.r2_id "
    "LEFT JOIN users AS r3 ON r3.id = matches.r3_id "
    "LEFT JOIN users AS r4 ON r4.id = matches.r4_id "
    "LEFT JOIN users AS r5 ON r5.id = matches.r5_id "
    "LEFT JOIN users AS r6 ON r6.id = matches.r6_id "
    "LEFT JOIN users AS b1 ON b1.id = matches.b1_id "
    "LEFT JOIN users AS b2 ON b2.id = matches.b2_id "
    "LEFT JOIN users AS b3 ON b3.id = matches.b3_id "
    "LEFT JOIN users AS b4 ON b4.id = matches.b4_id "
    "LEFT JOIN users AS b5 ON b5.id = matches.b5_id "
    "LEFT JOIN users AS b6 ON b6.id = matches.b6_id "

    "LEFT JOIN seasons_matches ON seasons_matches.match_id = matches.id "
    "LEFT JOIN seasons AS season ON season.id = seasons_matches.season_id "

    "WHERE matches.id = $1 "
    "LIMIT 1; "
)
get_user_matches = db.prepare('''
        SELECT
             matches.id, r_score, b_score, duration, validated_by, datetime,
            season.id as season$id, season.name as season$name,

        CASE
            -- OUPUT OF MATCH FOR USER ID
            WHEN (r_score > b_score AND (r1_id = $1 OR r2_id = $1 OR r3_id = $1 OR r4_id = $1 OR r5_id = $1 OR r6_id = $1)
                OR 
                (r_score < b_score AND (b1_id = $1 OR b2_id = $1 OR b3_id = $1 OR b4_id = $1 OR b5_id = $1 OR b6_id = $1))) THEN 'win'
            WHEN r_score = b_score THEN 'tie'
            ELSE 'lose'
        END AS output

        FROM matches 

        LEFT JOIN seasons_matches 
        ON matches.id = seasons_matches.match_id 
        LEFT JOIN seasons AS season 
        ON season.id = seasons_matches.season_id 

        WHERE 
        b1_id = $1 OR 
        b2_id = $1 OR 
        b3_id = $1 OR 
        b4_id = $1 OR 
        b5_id = $1 OR 
        b6_id = $1 OR 
        r1_id = $1 OR 
        r2_id = $1 OR 
        r3_id = $1 OR 
        r4_id = $1 OR 
        r5_id = $1 OR 
        r6_id = $1 

        ORDER BY matches.id DESC;
    ''')

get_ranked_users_musigma_team = db.prepare('''
    SELECT *, RANK() OVER (ORDER BY res.exposition DESC)
    FROM (
        SELECT DISTINCT ON (user_id) *
        FROM musigma_team
        WHERE (season_id = $1 OR ($1 IS NULL AND season_id IS NULL))
        ORDER BY user_id, id DESC
    ) AS res
    LEFT JOIN users ON users.id = res.user_id;
''')

create_stats = db.prepare(
    "INSERT INTO statistics (match_id, user_id, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) "
    "RETURNING id")
delete_match = db.prepare("DELETE FROM matches WHERE id = $1")
delete_match_stats = db.prepare("DELETE FROM statistics WHERE match_id = $1")
remove_match_season = db.prepare("DELETE FROM seasons_matches WHERE match_id = $1")

# ------------------------- PENDING MATCHES
create_pending_match = db.prepare(
    "INSERT INTO matches_pending (b_score, r_score, duration, datetime, "
    "b1_pseudo, b2_pseudo, b3_pseudo, b4_pseudo, b5_pseudo, b6_pseudo, "
    "r1_pseudo, r2_pseudo, r3_pseudo, r4_pseudo, r5_pseudo, r6_pseudo) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16) "
    "RETURNING id")
create_pending_stats = db.prepare(
    "INSERT INTO statistics_pending (match_id, user_pseudo, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) "
    "RETURNING id")
count_pending_stats_for_user_by_match = db.prepare("SELECT COUNT(*) FROM statistics_pending WHERE match_id = $1 AND user_pseudo = $2")
count_user_in_pending_match = db.prepare(
    "SELECT COUNT(*) "
    "FROM matches_pending "
    "WHERE id = $1 AND ("
    "b1_pseudo = $2 OR "
    "b2_pseudo = $2 OR "
    "b3_pseudo = $2 OR "
    "b4_pseudo = $2 OR "
    "b5_pseudo = $2 OR "
    "b6_pseudo = $2 OR "
    "r1_pseudo = $2 OR "
    "r2_pseudo = $2 OR "
    "r3_pseudo = $2 OR "
    "r4_pseudo = $2 OR "
    "r5_pseudo = $2 OR "
    "r6_pseudo = $2)")
get_pending_matches = db.prepare("SELECT * FROM matches_pending")
get_last_pending_match = db.prepare("SELECT * FROM matches_pending ORDER BY id DESC LIMIT 1")
get_pending_match_by_id = db.prepare(
    "SELECT matches_pending.id as id, r_score, b_score, duration, datetime,  "
    "r1.id as r1$id, r1.user_pseudo as r1$user_pseudo, r1.score as r1$score, r1.tags as r1$tags, r1.popped as r1$popped, r1.grabs as r1$grabs, r1.drops as r1$drops, r1.hold as r1$hold, r1.captures as r1$captures, r1.prevent as r1$prevent, r1.returns as r1$returns, r1.support as r1$support, r1.pups as r1$pups, "
    "r2.id as r2$id, r2.user_pseudo as r2$user_pseudo, r2.score as r2$score, r2.tags as r2$tags, r2.popped as r2$popped, r2.grabs as r2$grabs, r2.drops as r2$drops, r2.hold as r2$hold, r2.captures as r2$captures, r2.prevent as r2$prevent, r2.returns as r2$returns, r2.support as r2$support, r2.pups as r2$pups, "
    "r3.id as r3$id, r3.user_pseudo as r3$user_pseudo, r3.score as r3$score, r3.tags as r3$tags, r3.popped as r3$popped, r3.grabs as r3$grabs, r3.drops as r3$drops, r3.hold as r3$hold, r3.captures as r3$captures, r3.prevent as r3$prevent, r3.returns as r3$returns, r3.support as r3$support, r3.pups as r3$pups, "
    "r4.id as r4$id, r4.user_pseudo as r4$user_pseudo, r4.score as r4$score, r4.tags as r4$tags, r4.popped as r4$popped, r4.grabs as r4$grabs, r4.drops as r4$drops, r4.hold as r4$hold, r4.captures as r4$captures, r4.prevent as r4$prevent, r4.returns as r4$returns, r4.support as r4$support, r4.pups as r4$pups, "
    "r5.id as r5$id, r5.user_pseudo as r5$user_pseudo, r5.score as r5$score, r5.tags as r5$tags, r5.popped as r5$popped, r5.grabs as r5$grabs, r5.drops as r5$drops, r5.hold as r5$hold, r5.captures as r5$captures, r5.prevent as r5$prevent, r5.returns as r5$returns, r5.support as r5$support, r5.pups as r5$pups, "
    "r6.id as r6$id, r6.user_pseudo as r6$user_pseudo, r6.score as r6$score, r6.tags as r6$tags, r6.popped as r6$popped, r6.grabs as r6$grabs, r6.drops as r6$drops, r6.hold as r6$hold, r6.captures as r6$captures, r6.prevent as r6$prevent, r6.returns as r6$returns, r6.support as r6$support, r6.pups as r6$pups, "
    "b1.id as b1$id, b1.user_pseudo as b1$user_pseudo, b1.score as b1$score, b1.tags as b1$tags, b1.popped as b1$popped, b1.grabs as b1$grabs, b1.drops as b1$drops, b1.hold as b1$hold, b1.captures as b1$captures, b1.prevent as b1$prevent, b1.returns as b1$returns, b1.support as b1$support, b1.pups as b1$pups, "
    "b2.id as b2$id, b2.user_pseudo as b2$user_pseudo, b2.score as b2$score, b2.tags as b2$tags, b2.popped as b2$popped, b2.grabs as b2$grabs, b2.drops as b2$drops, b2.hold as b2$hold, b2.captures as b2$captures, b2.prevent as b2$prevent, b2.returns as b2$returns, b2.support as b2$support, b2.pups as b2$pups, "
    "b3.id as b3$id, b3.user_pseudo as b3$user_pseudo, b3.score as b3$score, b3.tags as b3$tags, b3.popped as b3$popped, b3.grabs as b3$grabs, b3.drops as b3$drops, b3.hold as b3$hold, b3.captures as b3$captures, b3.prevent as b3$prevent, b3.returns as b3$returns, b3.support as b3$support, b3.pups as b3$pups, "
    "b4.id as b4$id, b4.user_pseudo as b4$user_pseudo, b4.score as b4$score, b4.tags as b4$tags, b4.popped as b4$popped, b4.grabs as b4$grabs, b4.drops as b4$drops, b4.hold as b4$hold, b4.captures as b4$captures, b4.prevent as b4$prevent, b4.returns as b4$returns, b4.support as b4$support, b4.pups as b4$pups, "
    "b5.id as b5$id, b5.user_pseudo as b5$user_pseudo, b5.score as b5$score, b5.tags as b5$tags, b5.popped as b5$popped, b5.grabs as b5$grabs, b5.drops as b5$drops, b5.hold as b5$hold, b5.captures as b5$captures, b5.prevent as b5$prevent, b5.returns as b5$returns, b5.support as b5$support, b5.pups as b5$pups, "
    "b6.id as b6$id, b6.user_pseudo as b6$user_pseudo, b6.score as b6$score, b6.tags as b6$tags, b6.popped as b6$popped, b6.grabs as b6$grabs, b6.drops as b6$drops, b6.hold as b6$hold, b6.captures as b6$captures, b6.prevent as b6$prevent, b6.returns as b6$returns, b6.support as b6$support, b6.pups as b6$pups "
    "FROM matches_pending  "
    "LEFT JOIN statistics_pending AS r1 ON r1.match_id = matches_pending.id AND r1.user_pseudo = matches_pending.r1_pseudo "
    "LEFT JOIN statistics_pending AS r2 ON r2.match_id = matches_pending.id AND r2.user_pseudo = matches_pending.r2_pseudo "
    "LEFT JOIN statistics_pending AS r3 ON r3.match_id = matches_pending.id AND r3.user_pseudo = matches_pending.r3_pseudo "
    "LEFT JOIN statistics_pending AS r4 ON r4.match_id = matches_pending.id AND r4.user_pseudo = matches_pending.r4_pseudo "
    "LEFT JOIN statistics_pending AS r5 ON r5.match_id = matches_pending.id AND r5.user_pseudo = matches_pending.r5_pseudo "
    "LEFT JOIN statistics_pending AS r6 ON r6.match_id = matches_pending.id AND r6.user_pseudo = matches_pending.r6_pseudo "
    "LEFT JOIN statistics_pending AS b1 ON b1.match_id = matches_pending.id AND b1.user_pseudo = matches_pending.b1_pseudo "
    "LEFT JOIN statistics_pending AS b2 ON b2.match_id = matches_pending.id AND b2.user_pseudo = matches_pending.b2_pseudo "
    "LEFT JOIN statistics_pending AS b3 ON b3.match_id = matches_pending.id AND b3.user_pseudo = matches_pending.b3_pseudo "
    "LEFT JOIN statistics_pending AS b4 ON b4.match_id = matches_pending.id AND b4.user_pseudo = matches_pending.b4_pseudo "
    "LEFT JOIN statistics_pending AS b5 ON b5.match_id = matches_pending.id AND b5.user_pseudo = matches_pending.b5_pseudo "
    "LEFT JOIN statistics_pending AS b6 ON b6.match_id = matches_pending.id AND b6.user_pseudo = matches_pending.b6_pseudo "
    "WHERE matches_pending.id = $1 "
    "LIMIT 1; "
)
delete_pending_match = db.prepare("DELETE FROM matches_pending WHERE id = $1")
delete_pending_match_stats = db.prepare("DELETE FROM statistics_pending WHERE match_id = $1")

# ------------------------- SEASONS
get_seasons = db.prepare("SELECT * FROM seasons")
get_season_matches = db.prepare(
    "SELECT matches.id as id,  r_score, b_score, datetime, "
    "matches.b1_id, matches.b2_id, matches.b3_id, matches.b4_id, matches.b5_id, matches.b6_id, "
    "matches.r1_id, matches.r2_id, matches.r3_id, matches.r4_id, matches.r5_id, matches.r6_id, "
    "validator.id as validator$id, validator.pseudo as validator$pseudo, validator.usual_pseudos as validator$usual_pseudos "
    "FROM matches "
    "LEFT JOIN users AS validator ON validated_by = validator.id "
    "INNER JOIN seasons_matches ON matches.id = seasons_matches.match_id WHERE seasons_matches.season_id = $1")
get_season_by_id = db.prepare("SELECT * FROM seasons WHERE id = $1")
get_running_season = db.prepare("SELECT * FROM seasons where running = true LIMIT 1")
count_running_seasons = db.prepare("SELECT COUNT(*) FROM seasons WHERE running = true")
add_season_match = db.prepare("INSERT INTO seasons_matches (season_id, match_id) VALUES ($1, $2)")
update_season_match_count = db.prepare("UPDATE seasons SET played_matches = played_matches + 1 WHERE id = $1")
create_season = db.prepare("INSERT INTO seasons (name, max_time, max_matches, start_time) VALUES ($1, $2, $3, $4) RETURNING id")
terminate_season = db.prepare("UPDATE seasons SET running = false, end_time = $2 WHERE id = $1")

# ------------------------- CUSTOM STATS
get_user_match_stats = db.prepare('''
    SELECT 
        -- NB MATCHES PLAYED / WON / LOST
        COUNT(*) AS matches_played,
        COUNT(
            CASE WHEN (r_score > b_score AND (r1_id = $1 OR r2_id = $1 OR r3_id = $1 OR r4_id = $1 OR r5_id = $1 OR r6_id = $1))
                    OR 
                    (r_score < b_score AND (b1_id = $1 OR b2_id = $1 OR b3_id = $1 OR b4_id = $1 OR b5_id = $1 OR b6_id = $1)) THEN 1
            END
        ) AS wins,
        COUNT(
            CASE WHEN r_score = b_score THEN 1 END
        ) as ties,
        COUNT(
            CASE WHEN (r_score < b_score AND (r1_id = $1 OR r2_id = $1 OR r3_id = $1 OR r4_id = $1 OR r5_id = $1 OR r6_id = $1))
                    OR 
                    (r_score > b_score AND (b1_id = $1 OR b2_id = $1 OR b3_id = $1 OR b4_id = $1 OR b5_id = $1 OR b6_id = $1)) THEN 1
            END
        ) AS losses,

        -- AVERAGE MATCH DURATION
        AVG(duration) AS match_duration_avg,
        SUM(duration) AS time_played,
        
        -- AVERAGE SCORE OF USER'S TEAM
        AVG(
            CASE WHEN (r1_id = $1 OR r2_id = $1 OR r3_id = $1 OR r4_id = $1 OR r5_id = $1 OR r6_id = $1) THEN r_score
                WHEN (b1_id = $1 OR b2_id = $1 OR b3_id = $1 OR b4_id = $1 OR b5_id = $1 OR b6_id = $1) THEN b_score
            end
        ) AS team_score_avg

    FROM matches

    WHERE 
    b1_id = $1 OR 
    b2_id = $1 OR 
    b3_id = $1 OR 
    b4_id = $1 OR 
    b5_id = $1 OR 
    b6_id = $1 OR 
    r1_id = $1 OR 
    r2_id = $1 OR 
    r3_id = $1 OR 
    r4_id = $1 OR 
    r5_id = $1 OR 
    r6_id = $1
''')
# MISSES HOLD AND PREVENT
get_user_custom_stats = db.prepare('''

SELECT * FROM (
    -- TO GET ONLY SPECIFIC USER
    SELECT *, 
        -- TO ADD RANKS
        RANK() OVER (ORDER BY stats.score_avg DESC) AS score_rank,
        RANK() OVER (ORDER BY stats.tags_avg DESC) AS tags_rank,
        -- INVERTED
        RANK() OVER (ORDER BY stats.popped_avg ASC) AS popped_rank,
        RANK() OVER (ORDER BY stats.grabs_avg DESC) AS grabs_rank,
        -- INVERTED
        RANK() OVER (ORDER BY stats.drops_avg ASC) AS drops_rank,
        RANK() OVER (ORDER BY stats.captures_avg DESC) AS captures_rank,
        RANK() OVER (ORDER BY stats.pups_avg DESC) AS pups_rank,
        RANK() OVER (ORDER BY stats.support_avg DESC) AS support_rank,
        RANK() OVER (ORDER BY stats.returns_avg DESC) AS returns_rank,
        RANK() OVER (ORDER BY stats.hold_avg DESC) AS hold_rank,
        RANK() OVER (ORDER BY stats.prevent_avg DESC) AS prevent_rank,
        RANK() OVER (ORDER BY stats.grabs_eff DESC) AS grabs_eff_rank,
        -- INVERTED
        RANK() OVER (ORDER BY stats.hold_eff ASC) AS hold_eff_rank,
        -- INVERTED
        RANK() OVER (ORDER BY stats.captures_time ASC) AS captures_time_rank

        FROM (
            -- STATS COMPUTATIONS
            SELECT 
                user_id,
                AVG(score) AS score_avg,
                (AVG(score) - (SELECT AVG(score) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(scores_avg) - MIN(scores_avg) FROM (
                        SELECT AVG(score) AS scores_avg FROM statistics GROUP BY user_id
                        )  AS scores_avg
                    ) AS score_rating,

                AVG(tags) AS tags_avg,
                (AVG(tags) - (SELECT AVG(tags) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(tags_avg) - MIN(tags_avg) FROM (
                        SELECT AVG(tags) AS tags_avg FROM statistics GROUP BY user_id
                        )  AS tags_avg
                    ) AS tags_rating,

                AVG(popped) AS popped_avg,
                -- INVERTED
                ((SELECT AVG(popped) AS avg FROM statistics GROUP BY user_id ORDER BY avg DESC LIMIT 1) - AVG(popped)) / (
                    SELECT MAX(popped_avg) - MIN(popped_avg) FROM (
                        SELECT AVG(popped) AS popped_avg FROM statistics GROUP BY user_id
                        )  AS popped_avg
                    ) AS popped_rating,

                
                AVG(grabs) AS grabs_avg,
                (AVG(grabs) - (SELECT AVG(grabs) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(grabs_avg) - MIN(grabs_avg) FROM (
                        SELECT AVG(grabs) AS grabs_avg FROM statistics GROUP BY user_id
                        )  AS grabs_avg
                    ) AS grabs_rating,

                
                AVG(drops) AS drops_avg,
                -- INVERTED
                ((SELECT AVG(drops) AS avg FROM statistics GROUP BY user_id ORDER BY avg DESC LIMIT 1) - AVG(drops)) / (
                    SELECT MAX(drops_avg) - MIN(drops_avg) FROM (
                        SELECT AVG(drops) AS drops_avg FROM statistics GROUP BY user_id
                        )  AS drops_avg
                    ) AS drops_rating,

                AVG(captures) AS captures_avg,
                (AVG(captures) - (SELECT AVG(captures) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(captures_avg) - MIN(captures_avg) FROM (
                        SELECT AVG(captures) AS captures_avg FROM statistics GROUP BY user_id
                        )  AS captures_avg
                    ) AS captures_rating,
                
                AVG(pups) AS pups_avg,
                (AVG(pups) - (SELECT AVG(pups) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(pups_avg) - MIN(pups_avg) FROM (
                        SELECT AVG(pups) AS pups_avg FROM statistics GROUP BY user_id
                        )  AS pups_avg
                    ) AS pups_rating,

                AVG(support) AS support_avg,
                (AVG(support) - (SELECT AVG(support) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(support_avg) - MIN(support_avg) FROM (
                        SELECT AVG(support) AS support_avg FROM statistics GROUP BY user_id
                        )  AS support_avg
                    ) AS support_rating,

                AVG(returns) AS returns_avg,
                (AVG(returns) - (SELECT AVG(returns) AS avg FROM statistics GROUP BY user_id ORDER BY avg ASC LIMIT 1)) / (
                    SELECT MAX(returns_avg) - MIN(returns_avg) FROM (
                        SELECT AVG(returns) AS returns_avg FROM statistics GROUP BY user_id
                        ) AS returns_avg
                    ) AS returns_rating,

                -- EFFECTIVENESS
                SUM(CAST(captures AS decimal)) / SUM(grabs) AS grabs_eff,
                SUM(hold) / SUM(grabs) AS hold_eff,
                SUM(hold) / NULLIF(SUM(captures),0) AS captures_time,

                AVG(hold) AS hold_avg,
                AVG(prevent) AS prevent_avg

            FROM statistics

            GROUP BY user_id
        ) AS stats
    ) AS results
    WHERE user_id = $1
''')

def get_ranking(stat, method, season_id):
    season_id = season_id if season_id else 'NULL'

    return db.prepare('''
    SELECT user_id, pseudo, value, RANK() OVER (ORDER BY res.value DESC) FROM (
        SELECT user_id, {}({}) AS value FROM statistics
        LEFT JOIN seasons_matches on seasons_matches.match_id = statistics.match_id
        WHERE (season_id = {} OR ({} IS NULL AND season_id IS NULL))
        GROUP BY user_id
    ) AS res
    LEFT JOIN users ON users.id = res.user_id;
    '''.format(method, stat, season_id, season_id))()

# ------------------------- µσ-ranking
get_user_musigma_team = db.prepare("SELECT * FROM musigma_team WHERE user_id = $1 AND (season_id = $2 OR ($2 IS NULL AND season_id IS NULL)) ORDER BY id DESC LIMIT 1")
create_user_musigma_team = db.prepare("INSERT INTO musigma_team (user_id, match_id, season_id, exposition, mu, sigma) VALUES ($1, $2, $3, $4, $5, $6)")
get_all_user_musigma_rankings = db.prepare('''
    SELECT * FROM (
        SELECT user_id, exposition, mu, sigma, seasons.id AS season_id, seasons.name AS season_name, 
            RANK() OVER (PARTITION BY season_id ORDER BY res.exposition DESC)
        FROM(
            SELECT DISTINCT ON(user_id, season_id) *
            FROM musigma_team
            ORDER BY user_id, season_id, id DESC
        ) AS res
        LEFT JOIN seasons on seasons.id = res.season_id
        LEFT JOIN users ON users.id = res.user_id
        ORDER BY season_id DESC
        ) AS res
    WHERE user_id = $1;
''')
get_user_musigma_team_history = db.prepare('''
    SELECT musigma_team.*, m.datetime FROM musigma_team
    LEFT JOIN matches AS m ON m.id = musigma_team.match_id
    WHERE user_id = $1
    ORDER BY id, season_id, match_id DESC;
''')

# ========================= UTILS
# ROW CONVERTER MONKEY PATCHING
def to_dic(row):
    dic = {}
    for key in row.keys():
        dic[key] = row.get(key)
    return dic


# UNMANGLER
# we mangle 'joins' name and nested data with $ in SQl 'AS'.
# This function recursively nests data according to this.
def unmangle(row):
    for key in list(row.keys()):
        index = key.find('$')
        if index != -1:
            parent = key[0:index]
            child = key[index + 1:]
            if parent not in row.keys():
                row[parent] = {}
                row[parent][child] = row[key]
            row[parent][child] = row[key]
            unmangle(row[parent])
    return row


# TO_JSON
def row_to_json(row):
    return unmangle(to_dic(row))


def array_to_json(rows):
    json = []
    for row in rows:
        if isinstance(row, postgresql.types.Row):
            json.append(row_to_json(row))
    return json


def to_json(data):
    if isinstance(data, list):
        return array_to_json(data)
    elif isinstance(data, postgresql.types.Row):
        return row_to_json(data)
    elif data is None:
        return None
    else:
        raise TypeError("Invalid input type.")
