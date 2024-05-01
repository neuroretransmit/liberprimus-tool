import json
from configparser import ConfigParser
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

TABLE_NAME ="solution_attempts"

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def connect(config=load_config()):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def insert_solution_attempt(section, nums, scheme, key, shift, max_confidence, max_confidence_lang, skips, excludes):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO {TABLE_NAME} (section, nums, scheme, key, shift, max_confidence, max_confidence_lang, skips, excludes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                     (section, json.dumps(nums), scheme, key, shift, max_confidence, max_confidence_lang, json.dumps(skips), json.dumps(excludes)))
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    conn.close()


def solution_exists(section, nums, scheme, key, shift, skips, excludes):
    conn = connect(load_config())
    cursor = conn.cursor()
    skips = json.dumps(skips) if skips else None
    excludes = json.dumps(excludes) if excludes else None
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE section = %s AND nums @> %s AND scheme = %s AND key = %s AND shift = %s AND skips @> %s AND excludes @> %s;",
                 (section, json.dumps(nums), scheme, key, shift, skips, excludes))
    # The UNIQUE constraint is specified by all these columns so no need for fetchall
    data = cursor.fetchone()
    conn.close()
    if data is not None:
        return True
    return False

