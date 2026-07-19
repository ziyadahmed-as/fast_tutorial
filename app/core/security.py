"""Password hashing and verification helpers."""

import base64
import hashlib
import secrets
from typing import Final


_ITERATIONS: Final[int] = 100_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _ITERATIONS,
    )
    salt_b64 = base64.b64encode(salt).decode("ascii")
    derived_b64 = base64.b64encode(derived_key).decode("ascii")
    return f"pbkdf2_sha256${_ITERATIONS}${salt_b64}${derived_b64}"


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash.startswith("pbkdf2_sha256$"):
        return False

    _, iterations_str, salt_b64, derived_b64 = password_hash.split("$", 3)
    try:
        iterations = int(iterations_str)
    except ValueError:
        return False

    salt = base64.b64decode(salt_b64.encode("ascii"))
    expected = base64.b64decode(derived_b64.encode("ascii"))
    actual = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return secrets.compare_digest(actual, expected)
