import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "expense_manager"
    )

    if connection.is_connected():
        print("Connection Successful!")
    else:
        print("Failed to connect")

    cursor= connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called for {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s",(expense_date,))
        expenses_by_date = cursor.fetchall()
        return expenses_by_date

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called for {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s",(expense_date,))
        print(f"Expense on date {expense_date} has been deleted successfully!")

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called with data : {expense_date}, amount : {amount},category : {category},notes : {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date,amount,category,notes) VALUES(%s,%s,%s,%s)",
            (expense_date,amount,category,notes)
            )
        print("Expenses updated Successfully!")

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start : {start_date}, end : {end_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            '''SELECT category,SUM(amount) as total 
                        FROM expenses 
                        WHERE expense_date BETWEEN %s and %s
                        GROUP BY category''',
            (start_date,end_date)
            )
        expenses_by_category = cursor.fetchall()
        return expenses_by_category


