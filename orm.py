# -*- coding: utf-8 -*-
# You wish ! ORM are for pussies.

import config
import postgresql
import postgresql.exceptions
import postgresql.types

secret = config.secret()
db = postgresql.open(secret.get('pg_uri'))


# ========================= SQL COMMANDS
# You can ask for any existing field, unused fields will be filtered out using view models.
# If you need to join, always specify AS and mangle names with $.

# ------------------------- USERS
create_user = db.prepare("INSERT INTO users (trigram, pseudo) VALUES ($1, $2) RETURNING id")
get_users = db.prepare("SELECT id, pseudo, usual_pseudos FROM users")
update_user = db.prepare("UPDATE users SET pseudo = $2, usual_pseudos = $3 WHERE id = $1")
get_user_by_id = db.prepare("SELECT * FROM users WHERE id = $1 LIMIT 1")
desactivate_user = db.prepare("UPDATE users SET is_active = false WHERE id = $1")

# ------------------------- MATCHES
create_match = db.prepare(
    "INSERT INTO matches (b_score, r_score, datetime, "
    "b1_id, b2_id, b3_id, b4_id, b5_id, b6_id, "
    "r1_id, r2_id, r3_id, r4_id, r5_id, r6_id, "
    "validated_by) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16) "
    "RETURNING id")
get_matches = db.prepare(
    "SELECT *, "
    "validator.id as validator$id, validator.pseudo as validator$pseudo "
    "FROM matches "
    "LEFT JOIN users AS validator ON validated_by = validator.id")
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
    "validator.id as validator$id, validator.pseudo as validator$pseudo "
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
    "WHERE matches.id = $1 "
    "LIMIT 1")
get_user_matches = db.prepare(
    "SELECT *, "
    "validator.id as validator$id, validator.pseudo as validator$pseudo "
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
get_pending_match_by_id = db.prepare("SELECT * FROM matches_pending WHERE id = $1")
get_pending_match_stats = db.prepare("SELECT * FROM statistics_pending WHERE match_id = $1")
delete_pending_match = db.prepare("DELETE FROM matches_pending WHERE id = $1")
delete_pending_match_stats = db.prepare("DELETE FROM statistics_pending WHERE match_id = $1")

# ------------------------- SEASONS
get_seasons = db.prepare("SELECT * FROM seasons")
get_seasons_matches = db.prepare("SELECT * FROM matches INNER JOIN seasons_matches ON matches.id = seasons_matches.match_id WHERE seasons_matches.season_id = $1")
get_season_by_id = db.prepare("SELECT * FROM seasons WHERE id = $1")
get_running_season = db.prepare("SELECT * FROM seasons where running = true LIMIT 1")
count_running_seasons = db.prepare("SELECT COUNT(*) FROM seasons")
add_season_match = db.prepare("INSERT INTO seasons_matches (season_id, match_id) VALUES ($1, $2)")
update_season_match_count = db.prepare("UPDATE seasons SET played_matches = played_matches + 1 WHERE id = $1")
create_season = db.prepare("INSERT INTO seasons (name, max_time, max_matches, start_time) VALUES ($1, $2, $3, $4) RETURNING id")
terminate_season = db.prepare("UPDATE seasons SET running = false, end_time = $2 WHERE id = $1")


# ========================= UTILS
# ROW CONVERTER MONKEY PATCHING
def to_dic(row):
    dic = {}
    for key in row.keys():
        dic[key] = row.get(key)
    return dic


# UNMANGLER
# we mangle 'joins' name and nested data with $ in SQl 'AS'.
# This function recursively nest data according to this.
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
