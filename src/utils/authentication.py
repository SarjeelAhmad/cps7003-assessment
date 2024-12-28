# authentication.py
from sqlalchemy.orm import Session
from database.models import User
from utils.encryption import verify_password

def authenticate_user(db: Session, username: str, password: str) -> User:
    """Authenticates a user by their username and password."""
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(user.password, password):
        return user
    return None

def authorize_user(user: User, required_role: str) -> bool:
    """Authorizes a user based on their role (assuming a role attribute exists)."""
    # This is a placeholder for role-based authorization logic.
    # Replace 'user.role' with the actual attribute that stores user roles.
    return user.role == required_role