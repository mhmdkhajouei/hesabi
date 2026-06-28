import sqlite3
import os

def create_connection():

    DB_PATH = os.environ.get("DB_PATH", "/app/app.db")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    
    return conn