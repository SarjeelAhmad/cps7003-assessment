# encryption.py
import hashlib
import os

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + hashed_password.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a provided password against the stored hashed password."""
    salt = bytes.fromhex(stored_password[:32])
    stored_hash = stored_password[32:]
    provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000).hex()
    return stored_hash == provided_hash