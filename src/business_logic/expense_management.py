# expense_management.py
from sqlalchemy.orm import Session
from database.models import Expense

def create_expense(db: Session, date, amount, category, description, user_id):
    """Creates a new expense entry in the database."""
    new_expense = Expense(date=date, amount=amount, category=category, description=description, user_id=user_id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

def get_expenses(db: Session, user_id: int):
    """Retrieves all expenses for a given user."""
    return db.query(Expense).filter(Expense.user_id == user_id).all()

def update_expense(db: Session, expense_id: int, amount: float = None, category: str = None, description: str = None):
    """Updates an existing expense entry in the database."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        if amount:
            expense.amount = amount
        if category:
            expense.category = category
        if description:
            expense.description = description
        db.commit()
        db.refresh(expense)
    return expense

def delete_expense(db: Session, expense_id: int):
    """Deletes an expense entry from the database."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        db.delete(expense)
        db.commit()
    return expense