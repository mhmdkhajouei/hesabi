from backend import service as srv
from backend import  repository as rep
from backend.conn_db  import create_connection


def create_app():

    conn = create_connection()

    services = {

        "transaction" : srv.TransactionService(rep.TransactionRepo(conn), rep.CategoryRepo(conn)),
        "category" : srv.CategoryService(rep.CategoryRepo(conn), rep.BudgetRepo(conn)),
        "budget" : srv.BudgetService(rep.BudgetRepo(conn), rep.CategoryRepo(conn)),
        "compute" : srv.ComputeService(rep.ComputeRepo(conn))

        }

    return conn,services

def run_test(services):


    print("\n--- SETUP: Adding categories with budgets ---")

    services["category"].add_category("fast foods", 2000000)

    services["category"].add_category("technology", 5000000)

    services["category"].add_category("transport", 1000000)

    print("\n--- ADD TRANSACTIONS ---")

    services["transaction"].add_transaction(40000000, "income", "2026-06-01", None, "")

    services["transaction"].add_transaction(150000, "expense", "2026-06-02", 1, "lunch")

    services["transaction"].add_transaction(200000, "expense", "2026-06-03", 1, "dinner")

    services["transaction"].add_transaction(3000000, "expense", "2026-06-04", 2, "keyboard")

    services["transaction"].add_transaction(500000, "expense", "2026-06-05", 3, "taxi")

    services["transaction"].add_transaction(20000000, "income", "2026-06-06", None, "freelance")

    print("\n--- EDIT TRANSACTIONS ---")

    services["transaction"].edit_transaction(2, amount=180000)

    services["transaction"].edit_transaction(3, note="team dinner")

    services["transaction"].edit_transaction(4, amount=3500000, transaction_date="2026-06-04")

    print("\n--- EDIT CATEGORY ---")

    services["category"].edit_category(3, category_name="health")

    print("\n--- EDIT BUDGET (via budget service) ---")

    services["budget"].edit_budget(1, budget_goal=3000000)

    print("\n--- COMPUTE RESULTS ---")

    print("Income:", services["compute"].income_balance())

    print("Expense:", services["compute"].expense_balance())

    print("Total:", services["compute"].total_balance())

    print("All categories balance:", services["compute"].categories_balance())

    print("Category 1 balance:", services["compute"].category_balance(1))

    print("Category 2 balance:", services["compute"].category_balance(2))

    print("\n--- DELETE TRANSACTION ---")

    services["transaction"].delete_transaction(5)

    print("\n--- DELETE CATEGORY (cascades budget, nulls transactions) ---")

    services["category"].delete_category(2)

    print("\n--- COMPUTE AFTER DELETES ---")

    print("Expense after delete:", services["compute"].expense_balance())

    print("All categories balance after delete:", services["compute"].categories_balance())

    print("\n--- VALIDATION ERROR SCENARIOS ---")

    try:

        services["transaction"].add_transaction(-100, "expense", "2026-06-01", None, "")

    except ValueError as e:

        print("Expected error (negative amount):", e)

    try:

        services["transaction"].add_transaction(100000, "income", "2026-06-01", 1, "")

    except ValueError as e:

        print("Expected error (income with category):", e)

    try:

        services["transaction"].add_transaction(100000, "expense", "2030-01-01", None, "")

    except ValueError as e:

        print("Expected error (future date):", e)

    try:

        services["transaction"].add_transaction(100000, "expense", "2026-06-01", 999, "")

    except ValueError as e:

        print("Expected error (nonexistent category):", e)

    try:

        services["category"].add_category("", 1000000)

    except ValueError as e:

        print("Expected error (empty category name):", e)

    try:

        services["category"].add_category("a" * 21, 1000000)

    except ValueError as e:

        print("Expected error (category name too long):", e)

    try:

        services["budget"].edit_budget(999, budget_goal=1000000)

    except ValueError as e:

        print("Expected error (nonexistent budget):", e)

    try:

        services["transaction"].delete_transaction(999)

    except ValueError as e:

        print("Expected error (nonexistent transaction):", e)

    try:

        services["transaction"].edit_transaction(1, amount=-500)

    except ValueError as e:

        print("Expected error (edit with negative amount):", e)


def run_server():
    pass

if __name__ == "__main__":

    conn,service = create_app()
    rep.clean_test_data(conn, "transactions", "budgets", "categories")
    #run_test(service)