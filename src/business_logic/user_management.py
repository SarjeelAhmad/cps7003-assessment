# user_management.py
from sqlalchemy.orm import Session
from database.models import User
from utils.encryption import hash_password

def create_user(db: Session, username: str, password: str, email: str):
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, username: str = None, email: str = None):
    user = get_user(db, user_id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user