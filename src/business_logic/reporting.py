# reporting.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Expense, Inventory, Sale

def generate_expense_report(db: Session, user_id: int):
    total_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar()
    return total_expenses

def generate_inventory_report(db: Session):
    inventory_items = db.query(Inventory).all()
    return inventory_items

def generate_sales_report(db: Session, user_id: int):
    total_sales = db.query(func.sum(Sale.amount)).filter(Sale.user_id == user_id).scalar()
    return total_sales

def generate_financial_summary(db: Session, user_id: int):
    total_expenses = generate_expense_report(db, user_id)
    total_sales = generate_sales_report(db, user_id)
    profit = total_sales - total_expenses if total_sales is not None and total_expenses is not None else None
    return {
        "total_expenses": total_expenses,
        "total_sales": total_sales,
        "profit": profit
    }