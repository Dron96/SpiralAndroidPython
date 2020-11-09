import psycopg2
from psycopg2 import OperationalError


def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database='spiral',
            user='dron',
            password='',
            host='127.0.0.1',
            port='5432',
        )
        print("Connection successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Successfully")
        return cursor
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def create_tables(connection):
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      first_name TEXT NOT NULL,
      second_name TEXT NOT NULL,
      middle_name TEXT NOT NULL,
      dob DATE,
      sex BOOLEAN,
      dominant_hand VARCHAR(1),
      diagnosis VARCHAR(20)
    )
    """
    execute_query(connection, create_users_table)

    create_users_table = """
        CREATE TABLE IF NOT EXISTS examination (
          id SERIAL PRIMARY KEY,
          user_id INTEGER NOT NULL,
          hand VARCHAR(1),
          type VARCHAR(2),
          bad_effects VARCHAR(6),
          data DOUBLE precision [][],
          FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """

    execute_query(connection, create_users_table)


conn = create_connection()
create_tables(conn)
query = """
SELECT table_name FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema','pg_catalog')
"""
print(execute_query(conn, query).fetchall())
conn.close()
