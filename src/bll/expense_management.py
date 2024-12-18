from src.dal.models import Expense
from src.dal.db_config import initialize_database, sessionmaker
from datetime import datetime

# Initialize the database session
Session = sessionmaker()
initialize_database()

def add_expense(user_id, amount, category, description, date=None):
    """Adds a new expense to the database."""
    session = Session()
    try:
        if date is None:
            date = datetime.now().date()
        new_expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        session.add(new_expense)
        session.commit()
        return {"success": "Expense added successfully."}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()

def view_expenses(user_id):
    """Fetches all expenses for a user."""
    session = Session()
    try:
        expenses = session.query(Expense).filter_by(user_id=user_id).all()
        if not expenses:
            return {"info": "No expenses found."}
        return [
            {
                "id": expense.id,
                "date": expense.date,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description
            } for expense in expenses
        ]
    finally:
        session.close()

def categorize_expenses(user_id):
    """Categorizes expenses by their category and sums up amounts."""
    session = Session()
    try:
        expenses = session.query(Expense).filter_by(user_id=user_id).all()
        if not expenses:
            return {"info": "No expenses found."}
        categorized = {}
        for expense in expenses:
            if expense.category in categorized:
                categorized[expense.category] += expense.amount
            else:
                categorized[expense.category] = expense.amount
        return categorized
    finally:
        session.close()
