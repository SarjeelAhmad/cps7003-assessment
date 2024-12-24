# cli.py
import sys
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database.database_config import engine, init_db
from business_logic.user_management import create_user, get_user, update_user, delete_user
from business_logic.expense_management import create_expense, get_expenses, delete_expense, update_expense
from business_logic.inventory_management import add_inventory_item, get_inventory_items, delete_inventory_item, \
    update_inventory_item
from business_logic.sales_tracking import record_sale, get_sales, delete_sale, update_sale
from business_logic.reporting import generate_financial_summary
from utils.authentication import authenticate_user

# Initialize the database
init_db()

# Create a new database session
Session = sessionmaker(bind=engine)
db = Session()

# Global variable to keep track of the currently logged-in user
current_user = None


def main():
    global current_user
    while True:
        print("Welcome to Brew and Bite Café Management System")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            login()
        elif choice == '2':
            signup()
        elif choice == '3':
            print("Exiting...")
            db.close()
            sys.exit()
        else:
            print("Invalid choice! Please try again.")


def login():
    global current_user
    print("Login")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = authenticate_user(db, username, password)
    if user:
        current_user = user
        print(f"Welcome, {current_user.username}!")
        user_menu()
    else:
        print("Invalid username or password. Please try again.")


def signup():
    print("Signup")
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    user = create_user(db, username, password, email)
    print(f"User created: {user.id}")


def user_menu():
    global current_user
    while True:
        print("1. User Management")
        print("2. Expense Management")
        print("3. Inventory Management")
        print("4. Sales Tracking")
        print("5. Reporting")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            user_management()
        elif choice == '2':
            expense_management()
        elif choice == '3':
            inventory_management()
        elif choice == '4':
            sales_tracking()
        elif choice == '5':
            reporting()
        elif choice == '6':
            print("Logging out...")
            current_user = None
            return
        else:
            print("Invalid choice! Please try again.")


def user_management():
    global current_user
    print("User Management")
    print("1. Update User")
    print("2. Delete User")
    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter new username (leave blank to skip): ")
        email = input("Enter new email (leave blank to skip): ")
        updated_user = update_user(db, current_user.id, username, email)
        if updated_user:
            print("User updated successfully!")
    elif choice == '2':
        delete_user(db, current_user.id)
        print("User deleted successfully!")
        current_user = None
        main()  # Return to main menu after deleting the user
    else:
        print("Invalid choice!")


def expense_management():
    global current_user
    print("Expense Management")
    print("1. Record Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    choice = input("Enter your choice: ")

    if choice == '1':
        date_str = input("Enter date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert string to date object
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        description = input("Enter description: ")
        expense = create_expense(db, date, amount, category, description, current_user.id)
        print(f"Expense recorded: {expense.id}")
    elif choice == '2':
        expenses = get_expenses(db, current_user.id)
        for expense in expenses:
            print(
                f"ID: {expense.id}, Date: {expense.date}, Amount: {expense.amount}, Category: {expense.category}, Description: {expense.description}")
    elif choice == '3':
        expense_id = int(input("Enter expense ID: "))
        amount = input("Enter new amount (leave blank to skip): ")
        category = input("Enter new category (leave blank to skip): ")
        description = input("Enter new description (leave blank to skip): ")
        expense = update_expense(db, expense_id, amount or None, category or None, description or None)
        if expense:
            print("Expense updated successfully!")
        else:
            print("Expense not found!")
    elif choice == '4':
        expense_id = int(input("Enter expense ID: "))
        expense = delete_expense(db, expense_id)
        if expense:
            print("Expense deleted successfully!")
        else:
            print("Expense not found!")
    else:
        print("Invalid choice!")


def inventory_management():
    global current_user
    print("Inventory Management")
    print("1. Add Inventory Item")
    print("2. View Inventory Items")
    print("3. Update Inventory Item")
    print("4. Delete Inventory Item")
    choice = input("Enter your choice: ")

    if choice == '1':
        item_name = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        cost = float(input("Enter cost: "))
        item = add_inventory_item(db, item_name, quantity, cost)
        print(f"Inventory item added: {item.id}")
    elif choice == '2':
        items = get_inventory_items(db)
        for item in items:
            print(f"ID: {item.id}, Name: {item.item_name}, Quantity: {item.quantity}, Cost: {item.cost}")
    elif choice == '3':
        item_id = int(input("Enter item ID: "))
        item_name = input("Enter new item name (leave blank to skip): ")
        quantity = input("Enter new quantity (leave blank to skip): ")
        cost = input("Enter new cost (leave blank to skip): ")
        item = update_inventory_item(db, item_id, item_name or None, quantity or None, cost or None)
        if item:
            print("Inventory item updated successfully!")
        else:
            print("Inventory item not found!")
    elif choice == '4':
        item_id = int(input("Enter item ID: "))
        item = delete_inventory_item(db, item_id)
        if item:
            print("Inventory item deleted successfully!")
        else:
            print("Inventory item not found!")
    else:
        print("Invalid choice!")


def sales_tracking():
    global current_user
    print("Sales Tracking")
    print("1. Record Sale")
    print("2. View Sales")
    print("3. Update Sale")
    print("4. Delete Sale")
    choice = input("Enter your choice: ")

    if choice == '1':
        date_str = input("Enter date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert string to date object
        amount = float(input("Enter amount: "))
        items_sold = input("Enter items sold: ")
        sale = record_sale(db, date, amount, items_sold, current_user.id)
        print(f"Sale recorded: {sale.id}")
    elif choice == '2':
        sales = get_sales(db, current_user.id)
        for sale in sales:
            print(f"ID: {sale.id}, Date: {sale.date}, Amount: {sale.amount}, Items Sold: {sale.items_sold}")
    elif choice == '3':
        sale_id = int(input("Enter sale ID: "))
        amount = input("Enter new amount (leave blank to skip): ")
        items_sold = input("Enter new items sold (leave blank to skip): ")
        sale = update_sale(db, sale_id, amount or None, items_sold or None)
        if sale:
            print("Sale updated successfully!")
        else:
            print("Sale not found!")
    elif choice == '4':
        sale_id = int(input("Enter sale ID: "))
        sale = delete_sale(db, sale_id)
        if sale:
            print("Sale deleted successfully!")
        else:
            print("Sale not found!")
    else:
        print("Invalid choice!")


def reporting():
    global current_user
    print("Reporting")
    summary = generate_financial_summary(db, current_user.id)
    print(f"Total Expenses: {summary['total_expenses']}")
    print(f"Total Sales: {summary['total_sales']}")
    print(f"Profit: {summary['profit']}")


if __name__ == "__main__":
    main()