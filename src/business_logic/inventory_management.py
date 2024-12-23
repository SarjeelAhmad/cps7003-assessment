# inventory_management.py
from sqlalchemy.orm import Session
from database.models import Inventory

def add_inventory_item(db: Session, item_name: str, quantity: int, cost: float):
    new_item = Inventory(item_name=item_name, quantity=quantity, cost=cost)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_inventory_items(db: Session):
    return db.query(Inventory).all()

def update_inventory_item(db: Session, item_id: int, item_name: str = None, quantity: int = None, cost: float = None):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if item:
        if item_name:
            item.item_name = item_name
        if quantity:
            item.quantity = quantity
        if cost:
            item.cost = cost
        db.commit()
        db.refresh(item)
    return item

def delete_inventory_item(db: Session, item_id: int):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item