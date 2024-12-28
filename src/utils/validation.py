# validation.py
import re

def validate_email(email: str) -> bool:
    """Validates an email address using a regex pattern."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_password(password: str) -> bool:
    """Validates a password (minimum 8 characters, including at least one letter and one number)."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True