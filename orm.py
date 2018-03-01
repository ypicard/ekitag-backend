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
get_users = db.prepare("SELECT id, pseudo, usual_pseudos, is_active FROM users")
update_user = db.prepare("UPDATE users SET pseudo = $2, usual_pseudos = $3 WHERE id = $1")
get_user_by_id = db.prepare("SELECT * FROM users WHERE id = $1 LIMIT 1")
get_user_by_trigram = db.prepare("SELECT * FROM users WHERE trigram = $1 LIMIT 1")
desactivate_user = db.prepare("UPDATE users SET is_active = false WHERE id = $1")
get_user_by_pseudo = db.prepare("SELECT id FROM USERS WHERE $1 = ANY(USUAL_PSEUDOS) OR PSEUDO = $1;")

# ------------------------- ADMIN
promote_user = db.prepare("UPDATE users SET is_admin = true, password = crypt($2, gen_salt('bf')) WHERE id = $1")
auth_admin = db.prepare("SELECT password = crypt($2, password) FROM users WHERE trigram = $1 AND is_admin = true")
block_admin = db.prepare("UPDATE users SET is_admin = false WHERE id = $1")

# ------------------------- MATCHES
create_match = db.prepare(
    "INSERT INTO matches (b_score, r_score, datetime, "
    "b1_id, b2_id, b3_id, b4_id, b5_id, b6_id, "
    "r1_id, r2_id, r3_id, r4_id, r5_id, r6_id, "
    "validated_by) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16) "
    "RETURNING id")
get_matches = db.prepare(
    "SELECT matches.id AS id,  matches.r_score, matches.b_score, matches.datetime,"
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
    "ON season.id = seasons_matches.season_id")
get_match_by_id = db.prepare(
    "SELECT matches.id as id, r_score, b_score, datetime, "
    "b1.id as b1$id, b1.pseudo as b1$pseudo, "
    "b2.id as b2$id, b2.pseudo as b2$pseudo, "
    "b3.id as b3$id, b3.pseudo as b3$pseudo, "
    "b4.id as b4$id, b4.pseudo as b4$pseudo, "
    "b5.id as b5$id, b5.pseudo as b5$pseudo, "
    "b6.id as b6$id, b6.pseudo as b6$pseudo, "
    "r1.id as r1$id, r1.pseudo as r1$pseudo, "
    "r2.id as r2$id, r2.pseudo as r2$pseudo, "
    "r3.id as r3$id, r3.pseudo as r3$pseudo, "
    "r4.id as r4$id, r4.pseudo as r4$pseudo, "
    "r5.id as r5$id, r5.pseudo as r5$pseudo, "
    "r6.id as r6$id, r6.pseudo as r6$pseudo, "
    "validator.id as validator$id, validator.pseudo as validator$pseudo, "
    "season.id as season$id, season.name as season$name "
    "FROM matches "
    "LEFT JOIN users AS b1 ON b1_id = b1.id "
    "LEFT JOIN users AS b2 ON b2_id = b2.id "
    "LEFT JOIN users AS b3 ON b3_id = b3.id "
    "LEFT JOIN users AS b4 ON b4_id = b4.id "
    "LEFT JOIN users AS b5 ON b5_id = b5.id "
    "LEFT JOIN users AS b6 ON b6_id = b6.id "
    "LEFT JOIN users AS r1 ON r1_id = r1.id "
    "LEFT JOIN users AS r2 ON r2_id = r2.id "
    "LEFT JOIN users AS r3 ON r3_id = r3.id "
    "LEFT JOIN users AS r4 ON r4_id = r4.id "
    "LEFT JOIN users AS r5 ON r5_id = r5.id "
    "LEFT JOIN users AS r6 ON r6_id = r6.id "
    "LEFT JOIN users AS validator ON validated_by = validator.id "
    "LEFT JOIN seasons_matches ON seasons_matches.match_id = matches.id "
    "LEFT JOIN seasons AS season ON season.id = seasons_matches.season_id "
    "WHERE matches.id = $1 "
    "LIMIT 1")
get_user_matches = db.prepare(
    "SELECT *, "
    "validator.id as validator$id, validator.pseudo as validator$pseudo, validator.usual_pseudos as validator$usual_pseudos "
    "FROM matches "
    "LEFT JOIN users AS validator ON validated_by = validator.id "
    "WHERE "
    "b1_id = $1 OR "
    "b2_id = $1 OR "
    "b3_id = $1 OR "
    "b4_id = $1 OR "
    "b5_id = $1 OR "
    "b6_id = $1 OR "
    "r1_id = $1 OR "
    "r2_id = $1 OR "
    "r3_id = $1 OR "
    "r4_id = $1 OR "
    "r5_id = $1 OR "
    "r6_id = $1")
create_stats = db.prepare(
    "INSERT INTO statistics (match_id, user_id, score, tags, popped, grabs, drops, hold, captures, prevent, returns, support, pups) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) "
    "RETURNING id")
get_match_stats = db.prepare("SELECT * from statistics where match_id = $1")
delete_match = db.prepare("DELETE FROM matches WHERE id = $1")
delete_match_stats = db.prepare("DELETE FROM statistics WHERE match_id = $1")
remove_match_season = db.prepare("DELETE FROM seasons_matches WHERE match_id = $1")

# ------------------------- PENDING MATCHES
create_pending_match = db.prepare(
    "INSERT INTO matches_pending (b_score, r_score, datetime, "
    "b1_pseudo, b2_pseudo, b3_pseudo, b4_pseudo, b5_pseudo, b6_pseudo, "
    "r1_pseudo, r2_pseudo, r3_pseudo, r4_pseudo, r5_pseudo, r6_pseudo) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15) "
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
get_pending_match_by_id = db.prepare(
    "SELECT matches_pending.id as id, r_score, b_score, datetime,  "
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
    "WHERE matches_pending.id = $1; "
)
get_pending_match_stats = db.prepare("SELECT * FROM statistics_pending WHERE match_id = $1")
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

# ------------------------- µσ-ranking
# create_user_team_musigma = db.prepare("INSERT INTO musigma_team (user_id, season_id, mu, sigma) VALUES ($1, $2, $3, $4) RETURNING id")
# create_user_team_global_musigma = lambda user_id, mu, sigma: create_user_team_musigma(user_id, None, mu, sigma)
# get_user_team_musigma = db.prepare("SELECT * FROM musigma_team WHERE user_id = $1 AND season_id = $2")
# get_user_team_global_musigma = lambda user_id, mu, sigma: get_user_team_musigma(user_id, None)
get_user_musigma_team = db.prepare("SELECT * FROM musigma_team WHERE user_id = $1 AND season_id = $2")
update_user_musigma_team = db.prepare("UPDATE musigma_team SET mu = $2, sigma = $3 WHERE user_id = $1 AND season_id = $2")
create_user_musigma_team = db.prepare("INSERT INTO musigma_team (user_id, mu, sigma, season_id) VALUES ($1, $2, $3, $4) RETURNING id")
upsert_user_musigma_team = db.prepare("INSERT INTO musigma_team (user_id, mu, sigma, season_id) VALUES ($1, $2, $3, $4) "
    "ON CONFLICT (user_id, season_id) DO UPDATE SET mu = $2, sigma = $3 RETURNING *")
# update_user_team_musigma = db.prepare("UPDATE musigma_team SET mu = $3, sigma = $4 WHERE user_id = $1 AND season_id = $2")
# update_user_team_global_musigma = lambda user_id, mu, sigma: update_user_team_musigma(user_id, None, mu, sigma)
# create_user_solo_musigma = db.prepare("INSERT INTO musigma_solo (user_id, season_id, mu, sigma) VALUES ($1, $2, $3, $4) RETURNING id")
# create_user_solo_global_musigma = lambda user_id, mu, sigma: create_user_solo_musigma(user_id, None, mu, sigma)
# get_user_solo_musigma = db.prepare("SELECT * FROM musigma_solo WHERE user_id = $1 AND season_id = $2")
# get_user_solo_global_musigma = lambda user_id, mu, sigma: get_user_solo_musigma(user_id, None)
# update_user_solo_musigma = db.prepare("UPDATE musigma_solo SET mu = $3, sigma = $4 WHERE user_id = $1 AND season_id = $2")
# update_user_solo_global_musigma = lambda user_id, mu, sigma: update_user_solo_musigma(user_id, None, mu, sigma)


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
