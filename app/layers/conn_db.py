import sqlite3

def create_connection():
    
    conn = sqlite3.connect("/Users/mohammad/Documents/Python/projects/Financial/app.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    
    return conn