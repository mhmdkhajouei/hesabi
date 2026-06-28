

class TransactionRepo():
    
    def __init__(self,conn):

        self.conn= conn
    
    
    def insert_transaction(self,amount,transactions_type,transaction_date,category_id,note):
        
        cursor = self.conn.cursor()
        cursor.execute('''             
        INSERT INTO transactions (amount,transaction_type,transaction_date,category_id,note)
        VALUES (?,?,?,?,?)''',
        (amount,transactions_type,transaction_date,category_id,note)
        )

        self.conn.commit()
        return cursor.lastrowid


    def update_transaction(self,transaction_id,kwargs):
    
        cursor = self.conn.cursor()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [transaction_id]
        cursor.execute(f"UPDATE transactions SET {set_clause} WHERE transaction_id = ? ", values)

        self.conn.commit()


    def delete_transaction(self,transaction_id):

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ? ", (transaction_id,))

        self.conn.commit()

    def check_transaction(self,transaction_id):

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT EXISTS(SELECT 1 FROM transactions WHERE transaction_id = ? )
        ''',
        (transaction_id,)
        )

        result = cursor.fetchone()
        return result[0]


    def get_transaction(self,transaction_id):

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT transaction_id, amount, transaction_type, transaction_date, category_id, note
        FROM transactions
        WHERE transaction_id = ?
        ''',
        (transaction_id,)
        )
        result = cursor.fetchone()

        return result


    def get_all_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT transaction_id, amount, transaction_type, transaction_date, category_id, note
            FROM transactions
            ORDER BY transaction_id ASC
        ''')
        return cursor.fetchall()


class CategoryRepo():

    def __init__(self,conn):
        
        self.conn= conn
    
    def insert_category(self,category_name):
        
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO categories (category_name)
        VALUES (?)
        ''',
        (category_name,)
        )

        self.conn.commit()
        return cursor.lastrowid


    def get_category(self,category_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT category_id, category_name 
        FROM categories
        WHERE category_id = (?)
        ''',
        (category_id,)
        )
        result = cursor.fetchone()
        return result


    def get_all_categories(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT categories.category_id, categories.category_name, budgets.budget_goal
        FROM categories
        JOIN budgets ON categories.category_id = budgets.category_id
        ORDER BY categories.category_id ASC
        ''')
        return cursor.fetchall()


    def check_category(self,category_id):

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT EXISTS(SELECT 1 FROM categories WHERE category_id = ? )
        ''',
        (category_id,)
        )

        result = cursor.fetchone()
        return result[0]


    def update_category(self,category_id,kwargs):

        cursor = self.conn.cursor()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [category_id]
        cursor.execute(f"UPDATE categories SET {set_clause} WHERE category_id = ?", values)

        self.conn.commit()


    def delete_category(self,category_id):

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM categories WHERE category_id = ?", (category_id,))

        self.conn.commit()


class BudgetRepo():

    def __init__(self,conn):
        
        self.conn = conn


    def insert_budget(self,budget_goal,category_id):

        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO budgets (budget_goal,category_id)
        VALUES (?,?)
        ''',
        (budget_goal,category_id)
        )

        self.conn.commit()
        return cursor.lastrowid


    def update_budget(self,budget_id,kwargs):

        cursor = self.conn.cursor()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [budget_id]
        cursor.execute(f"UPDATE budgets SET {set_clause} WHERE budget_id = ?", values)

        self.conn.commit()

    
    def delete_budget(self,budget_id):

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE budget_id = ?", (budget_id,))

        self.conn.commit()


    def check_budget(self,budget_id):

        cursor = self.conn.cursor()
        cursor.execute('''SELECT EXISTS(SELECT 1 FROM budgets WHERE budget_id = ? )
        ''',
        (budget_id,)
        )

        result = cursor.fetchone()
        return result[0]


    def get_budget(self,budget_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT budget_id, budget_goal, currency
        FROM budgets
        WHERE budget_id = (?)
        ''',
        (budget_id,)
        )
        result = cursor.fetchone()

        return result

    def get_budget_by_category(self, category_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT  budget_id, budget_goal
        FROM budgets
        WHERE category_id = (?)
        ''',
        (category_id,)
        )
        result = cursor.fetchone()
        return result

class ComputeRepo():

    def __init__(self,conn):

        self.conn = conn


    def get_amount(self,transaction_type):

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT sum(amount) FROM transactions WHERE transaction_type = ?
        ''',
        (transaction_type,)
        )
        result = cursor.fetchone()

        return result[0]


    def get_categories_balance(self):

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT categories.category_name, budgets.budget_goal, COALESCE(SUM(transactions.amount), 0) as spent
        FROM categories
        JOIN budgets ON categories.category_id = budgets.category_id
        LEFT JOIN transactions ON categories.category_id = transactions.category_id 
        AND transactions.transaction_type = 'expense'
        GROUP BY categories.category_id
        '''
        )
        result = cursor.fetchall()

        return result


    def get_category_balance(self,category_id):

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT categories.category_name, budgets.budget_goal, COALESCE(SUM(transactions.amount), 0) as spent
        FROM categories
        JOIN budgets ON categories.category_id = budgets.category_id
        LEFT JOIN transactions ON categories.category_id = transactions.category_id 
        AND transactions.transaction_type = 'expense'
        WHERE categories.category_id = ?
        GROUP BY categories.category_id
        ''',
        (category_id,)
        )
        result = cursor.fetchone()

        return result




def clean_test_data(conn, *table_names):
    cursor = conn.cursor()

    for table in table_names:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
 