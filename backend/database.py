import sqlite3

DB_NAME = "userDB.db"

def get_db_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables fetching rows as dictionaries
    return conn
