import psycopg2
import os


class DatabaseHelper:
    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def connect(self):
        """Return a connection to the database."""
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            return conn
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def execute_query(self, query, params=None, fetch=False):
        """Execute the given database query and return the results if needed."""
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if fetch:
                        return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def create_table(self):
        """Create the cart table if it does not exist."""
        self.execute_query(
            """CREATE TABLE IF NOT EXISTS cart (id SERIAL PRIMARY KEY, name TEXT, price NUMERIC, quantity NUMERIC)"""
        )
