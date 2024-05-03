import json
from configparser import ConfigParser
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

# TODO: Use global connection for execution speed

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
        cursor.execute(f"""INSERT INTO {TABLE_NAME} (section, nums, scheme, key, shift, max_confidence, max_confidence_lang, skips, excludes)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                     (section, json.dumps(nums), scheme, key, shift, max_confidence, max_confidence_lang, json.dumps(skips), json.dumps(excludes)))
        print(cursor.query)
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    conn.close()

# FIXME: We are getting a lot of unique constraint violations which means this query isn't working properly.
def solution_exists(section, nums, scheme, key, shift, skips, excludes):
    conn = connect(load_config())
    cursor = conn.cursor()
    nums = json.dumps(nums)
    skips = json.dumps(skips) if skips else None
    excludes = json.dumps(excludes) if excludes else None
    key_clause = ''
    if key is None:
        key_clause += 'AND key IS %s'
    else:
        key_clause += 'AND key = %s'
    sql = f"SELECT * FROM {TABLE_NAME} WHERE section = %s AND nums @> %s AND scheme = %s {key_clause} AND shift = %s"
    # Handle null for JSON columns
    if skips is None:
        sql += " AND skips = %s "
    else:
        sql += ' AND skips @> %s '
    if excludes is None:
        sql += " AND excludes = %s"
    else:
        sql += ' AND excludes %> %s'
    sql += ';'
    print(sql)
    cursor.execute(sql, (section, nums, scheme, key, shift, skips if skips else 'null', excludes if excludes else 'null'))
    print(cursor.query)
    # The UNIQUE constraint is specified by all these columns so no need for fetchall
    data = cursor.fetchone()
    print(data)
    conn.close()
    if data is not None:
        return True
    return False

