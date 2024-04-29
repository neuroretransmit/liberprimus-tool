import sqlite3
import json

DB_NAME = "solution_attempts.db"
TABLE_NAME ="solution_attempts"

conn = sqlite3.connect(DB_NAME, isolation_level=None)

def insert_solution_attempt(scheme, key, shift, max_confidence, max_confidence_lang, skips, excludes):
    conn.execute(f'INSERT INTO {TABLE_NAME} VALUES (NULL, ?, ?, ?, ?, ?, json(?), json(?))',
                 (scheme, key, shift, max_confidence, max_confidence_lang, json.dumps(skips), json.dumps(excludes)))
    conn.commit()

def solution_exists(scheme, key, shift, skips, excludes):
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, scheme, key, shift, json_extract(skips, '$'), json_extract(excludes, '$') FROM {TABLE_NAME} WHERE scheme = ? AND key = ? AND shift = ? AND skips = ? AND excludes = ?",
                 (scheme, key, shift, json.dumps(skips), json.dumps(excludes)))
    # The UNIQUE constraint is specified by all these columns so no need for fetchall
    data = cursor.fetchone()
    if data is not None:
        return True
    return False

