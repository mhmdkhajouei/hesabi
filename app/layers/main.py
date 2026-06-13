import service as srv
import repository as rep
from conn_db import create_connection


def create_app():

    conn = create_connection()

    services = {

        "transaction" : srv.TransactionService(rep.TransactionRepo(conn), rep.CategoryRepo(conn)),
        "category" : srv.CategoryService(rep.CategoryRepo(conn)),
        "budget" : srv.BudgetService(rep.BudgetRepo(conn), rep.CategoryRepo(conn)),
        "compute" : srv.ComputeService(rep.ComputeRepo(conn))

        }

    return conn,services

def run_test(services):

    services["category"].add_category("fast foods")
    services["category"].add_category("technology")
    services["transaction"].add_transaction(150000, "expense", "2026-06-04", 1, "this is first")
    services["transaction"].add_transaction(200000, "expense", "2026-06-02", 1, "this is second")
    services["transaction"].add_transaction(500000, "expense", "2026-06-06", 2, "this is third")
    services["transaction"].add_transaction(40000000, "income", "2026-05-12", None, "")
    services["budget"].add_budget(2500000, 1)
    services["budget"].add_budget(2500000, 2)
    services["transaction"].edit_transaction(1, amount=200000, transaction_date="2026-06-04",note="this is an edited transaction")
    #services["transaction"].delete_transaction(3)
    services["category"].edit_category(category_id=2, category_name="develop")
    #services["category"].delete_category(1)
    services["budget"].edit_budget(1, budget_goal= 3000000)
    services["budget"].delete_budget(2)
    print(services["compute"].categories_balance())
    print(services["compute"].category_balance(1))
    print(services["compute"].income_balance())
    print(services["compute"].expense_balance())


def run_server():
    pass

if __name__ == "__main__":

    conn,service = create_app()
    #rep.clean_test_data(conn, "transactions", "budgets", "categories")
    run_test(service)