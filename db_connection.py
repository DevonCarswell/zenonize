import sqlite3
from contextlib import contextmanager
import os

DB_PATH = os.path.join("db", "zenonize.db")

@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection handling and closure.
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(...)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    finally:
        conn.close()

# def init_db():
#     """Initialize database with required tables if they don't exist."""
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
        
#         # Create Players table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS players (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nickname TEXT UNIQUE NOT NULL,
#                 email_code TEXT,
#                 attempt_1 REAL,
#                 attempt_2 REAL,
#                 attempt_3 REAL,
#                 attempt_4 REAL,
#                 attempt_5 REAL
#             )
#         """)
        
#         # Create Leaderboard table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS leaderboard (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nickname TEXT UNIQUE NOT NULL,
#                 profit REAL NOT NULL
#             )
#         """)
        
#         conn.commit()
