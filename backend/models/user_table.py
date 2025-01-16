import sqlite3
from database import get_db_connection  # Import database connection

def create_users_table():
    """Creates the users table if it doesn't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                leave_balance INTEGER DEFAULT 30
            )
        ''')
        conn.commit()
        print("✅ Users table setup completed successfully.")

if __name__ == "__main__":
    create_users_table()  # Run this script to initialize the table
