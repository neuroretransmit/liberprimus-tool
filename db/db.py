import sqlite3
import json

DB_NAME = "solution_attempts.db"
TABLE_NAME ="solution_attempts"

conn = sqlite3.connect(DB_NAME, isolation_level=None)

def insert_solution_attempt(scheme, key, shift, max_confidence, max_confidence_lang, skips, excludes):
    conn.execute(f'INSERT INTO {TABLE_NAME} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)',
                 (scheme, key, shift, max_confidence, max_confidence_lang, json.dumps(skips), json.dumps(excludes)))
    conn.commit()
