import psycopg2
import os


def get_db_connection():
    """Return a connection to the database."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return None


def exec_db_query(query, params=None, fetch=False):
    """Execute the given database query and return the results if needed."""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
