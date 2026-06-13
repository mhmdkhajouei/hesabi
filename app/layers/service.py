import datetime as dt
import utils as ut


class TransactionService():

    def __init__(self, repo, category_repo):

        self.repo = repo
        self.category_repo = category_repo


    def _validate_amount(self, amount):

        if not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        if amount <= 0:
            raise ValueError("amount must be greater than zero")

        return amount

    def _validate_type(self, transactions_type):

        if not isinstance(transactions_type, str):
            raise ValueError("transaction type must be a string")
        transactions_type = ut.par_normalize(transactions_type)
        if transactions_type not in ['income', 'expense']:
            raise ValueError("transaction type is not valid")

        return transactions_type

    def _validate_date(self, transaction_date):

        transaction_date = ut.date_formater(transaction_date)
        if transaction_date.date() > dt.date.today():
            raise ValueError("transaction date cannot be in the future")

        return transaction_date

    def _validate_category_id(self, category_id, transactions_type):

        if category_id is None:
            return None
        if not isinstance(category_id, int):
            raise ValueError("category id must be an integer")
        if transactions_type == "income":
            raise ValueError("income transactions cannot reference a category")
        if not self.category_repo.check_category(category_id):
            raise ValueError("category does not exist")

        return category_id

    def _validate_note(self, note):

        if note == "" or note is None:
            return None
        note = ut.text_normalize(note)
        if len(note) > 250:
            raise ValueError("note cannot be greater than 250 characters")

        return note

    def _validate_transaction_id(self,transaction_id):

        if transaction_id is None:
            raise ValueError("transaction id can not be empty")
        if not isinstance(transaction_id, int):
            raise ValueError("transaction id must be an integer")
        if not self.repo.check_transaction(transaction_id):
            raise ValueError("transaction does not exist")

        return transaction_id

    def validate_transaction(self, amount, transactions_type, transaction_date, category_id, note):

        amount = self._validate_amount(amount)
        transactions_type = self._validate_type(transactions_type)
        transaction_date = self._validate_date(transaction_date)
        category_id = self._validate_category_id(
            category_id, transactions_type)
        note = self._validate_note(note)

        return amount, transactions_type, transaction_date, category_id, note


    def add_transaction(self, amount, transactions_type, transaction_date, category_id, note):

        clean_data = self.validate_transaction(
            amount, transactions_type, transaction_date, category_id, note)
        self.repo.insert_transaction(*clean_data)


    def edit_transaction(self,transaction_id,**kwargs):

        self._validate_transaction_id(transaction_id)
        if "amount" in kwargs:
            kwargs["amount"] = self._validate_amount(kwargs["amount"])
        if "transaction_type" in kwargs:
            kwargs["transaction_type"] = self._validate_type(kwargs["transaction_type"])
        if "transaction_date" in kwargs:
            kwargs["transaction_date"] = self._validate_date(kwargs["transaction_date"])
        if "category_id" in kwargs:
            if "transaction_type" in kwargs:
                current_type = kwargs["transaction_type"]
            else:
                current_type = self.repo.get_transaction(transaction_id)["transaction_type"]
            kwargs["category_id"] = self._validate_category_id(kwargs["category_id"],current_type)
        if "note" in kwargs:
            kwargs["note"] = self._validate_note(kwargs["note"])

        self.repo.update_transaction(transaction_id,kwargs)


    def delete_transaction(self,transaction_id):

        self._validate_transaction_id(transaction_id)
        self.repo.delete_transaction(transaction_id)


class CategoryService():

    def __init__(self, repo):
        self.repo = repo


    def _validate_name(self, category_name):

        category_name = ut.text_normalize(category_name)
        if category_name == "":
            raise ValueError("category name cannot be empty")
        if len(category_name) > 20:
            raise ValueError("category name cannot be more than 20 characters")

        return category_name

    def _validate_category_id(self, category_id):

        if category_id is None:
            raise ValueError("there is no category id entered !")
        if not isinstance(category_id, int):
            raise ValueError("category id must be an integer")
        if not self.repo.check_category(category_id):
            raise ValueError("this category id does not exsist")

        return category_id

    def add_category(self, category_name):

        category_name = self._validate_name(category_name)
        self.repo.insert_category(category_name)


    def edit_category(self,category_id,**kwargs):

        self._validate_category_id(category_id)
        if "category_name" in kwargs:
            kwargs["category_name"] = self._validate_name(kwargs["category_name"])

        self.repo.update_category(category_id, kwargs)


    def delete_category(self,category_id):

        self._validate_category_id(category_id)
        self.repo.delete_category(category_id)


class BudgetService():

    def __init__(self, repo, category_repo):

        self.repo = repo
        self.category_repo = category_repo


    def _validate_budget_goal(self, budget_goal):

        if not isinstance(budget_goal, int):
            raise ValueError("budget goal must be an integer")
        if budget_goal <= 0:
            raise ValueError("budget goal must be greater than zero")

        return budget_goal

    def _validate_category_id(self, category_id):

        if category_id is None:
            raise ValueError("you must reference a category")
        if not isinstance(category_id, int):
            raise ValueError("category id must be an integer")
        if not self.category_repo.check_category(category_id):
            raise ValueError("category does not exist")

        return category_id


    def _validate_budget_id(self,budget_id):

        if budget_id is None:
            raise ValueError("there is no budget id entered !")
        if not isinstance(budget_id, int):
            raise ValueError("budget_id must be an integer")
        if not self.repo.check_budget(budget_id):
            raise ValueError("this budget id does not exsist")

        return budget_id


    def validate_budget(self, budget_goal, category_id):

        budget_goal = self._validate_budget_goal(budget_goal)
        category_id = self._validate_category_id(category_id)

        return budget_goal, category_id


    def add_budget(self, budget_goal, category_id):

        clean_data = self.validate_budget(budget_goal, category_id)
        self.repo.insert_budget(*clean_data)


    def edit_budget(self,budget_id,**kwargs):

        self._validate_budget_id(budget_id)
        if "budget_goal" in kwargs:
            kwargs["budget_goal"] = self._validate_budget_goal(kwargs["budget_goal"])
        
        self.repo.update_budget(budget_id, kwargs)


    def delete_budget(self,budget_id):

        self._validate_budget_id(budget_id)
        self.repo.delete_budget(budget_id)


class ComputeService():

    
    def __init__(self,repo):

        self.repo = repo


    def income_balance(self):

        transaction_type = "income"
        result = self.repo.get_amount(transaction_type)

        return result


    def expense_balance(self):

        transaction_type = "expense"
        result = self.repo.get_amount(transaction_type)

        return result


    def total_balance(self):

        inc = self.repo.get_amount("income") or 0
        exp = self.repo.get_amount("expense") or 0
        total_result = inc - exp

        return total_result


    def category_balance(self,category_id):

        category_balance = self.repo.get_category_amount(category_id)
        if not category_balance:
            category_balance = []

        return category_balance


    def categories_balance(self):

        categories_balance = self.repo.get_categories_amount()
        if not categories_balance:
            categories_balance = 0

        return categories_balance