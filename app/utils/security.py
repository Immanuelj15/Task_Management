import hashlib
import hmac
import secrets


def generate_salt() -> str:
    """Generate a random 16-byte hex salt string."""
    return secrets.token_hex(16)


def hash_password(password: str, salt: str | None = None) -> str:
    """
    Hash a password using SHA-256 with a salt.
    Format stored: salt$hash
    """
    if salt is None:
        salt = generate_salt()
    salted = f"{salt}:{password}".encode("utf-8")
    pwd_hash = hashlib.sha256(salted).hexdigest()
    return f"{salt}${pwd_hash}"


def verify_password(plain_password: str, stored_password_hash: str) -> bool:
    """Verify a plain password against the stored salt$hash format."""
    if not stored_password_hash or "$" not in stored_password_hash:
        return False
    salt, expected_hash = stored_password_hash.split("$", 1)
    recalculated = hash_password(plain_password, salt=salt).split("$", 1)[1]
    return hmac.compare_digest(expected_hash, recalculated)
