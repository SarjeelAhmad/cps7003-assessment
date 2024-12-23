# sales_tracking.py
from sqlalchemy.orm import Session
from database.models import Sale

def record_sale(db: Session, date, amount, items_sold, user_id) -> Sale:
    """Records a new sale entry in the database."""
    new_sale = Sale(date=date, amount=amount, items_sold=items_sold, user_id=user_id)
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

def get_sales(db: Session, user_id: int):
    """Retrieves all sales for a given user."""
    return db.query(Sale).filter(Sale.user_id == user_id).all()

def update_sale(db: Session, sale_id: int, amount: float = None, items_sold: str = None):
    """Updates an existing sale entry in the database."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale:
        if amount:
            sale.amount = amount
        if items_sold:
            sale.items_sold = items_sold
        db.commit()
        db.refresh(sale)
    return sale

def delete_sale(db: Session, sale_id: int):
    """Deletes a sale entry from the database."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale:
        db.delete(sale)
        db.commit()
    return sale