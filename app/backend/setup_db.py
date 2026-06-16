from conn_db import create_connection

conn= create_connection()

cursor= conn.cursor()

cursor.execute("PRAGMA foreign_keys =ON;")


cursor.execute('''
               
    CREATE TABLE categories(
        category_id   INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL UNIQUE CHECK (length(category_name) <= 20)
        );
    ''')


cursor.execute('''
               
    CREATE TABLE budgets(
        budget_id     INTEGER PRIMARY KEY,
        budget_goal   INTEGER NOT NULL CHECK (budget_goal > 0),
        currency      TEXT NOT NULL DEFAULT 'TOMAN' CHECK (currency IN ('TOMAN')),
        category_id   INTEGER NOT NULL UNIQUE,
        
        FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE
        
        );
    ''')


cursor.execute('''

    CREATE TABLE transactions(
        
        transaction_id   INTEGER  PRIMARY KEY,
        amount           INTEGER  NOT NULL CHECK (amount > 0),
        transaction_type TEXT     NOT NULL CHECK (transaction_type IN ('expense','income')),
        currency         TEXT     NOT NULL DEFAULT 'TOMAN' CHECK (currency IN ('TOMAN')),
        transaction_date TEXT     NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        category_id      INTEGER,
        note             TEXT     CHECK (length(note) <= 225),
        
        FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE SET NULL
        
        );
    ''')
    
    
conn.commit()

conn.close()