from src.dal.models import User
from src.dal.db_config import initialize_database, sessionmaker

# Initialize the database session
Session = sessionmaker()
initialize_database()

def register_user(username, password, email):
    """Registers a new user in the system."""
    session = Session()
    try:
        if session.query(User).filter_by(username=username).first():
            return {"error": "Username already exists."}
        new_user = User(username=username, password=password, email=email)
        session.add(new_user)
        session.commit()
        return {"success": "User registered successfully."}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()

def update_user(user_id, username=None, email=None):
    """Updates user information."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found."}
        if username:
            user.username = username
        if email:
            user.email = email
        session.commit()
        return {"success": "User updated successfully."}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()

def delete_user(user_id):
    """Deletes a user by ID."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found."}
        session.delete(user)
        session.commit()
        return {"success": "User deleted successfully."}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()

def get_user(user_id):
    """Fetches a user by ID."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found."}
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    finally:
        session.close()
