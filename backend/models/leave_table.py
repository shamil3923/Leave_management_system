import sqlite3
from database import get_db_connection  # Import database connection

def create_leave_requests_table():
    """Creates the leave_requests table if it doesn't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leave_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                start_date TEXT,
                end_date TEXT,
                leave_days INTEGER,
                ai_decision TEXT,
                ai_explaination TEXT,  
                reason TEXT,
                submit_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        print("✅ Leave requests table setup completed successfully.")

if __name__ == "__main__":
    create_leave_requests_table()  # Run this script to initialize the table
