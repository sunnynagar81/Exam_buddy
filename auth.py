import hashlib
import hmac
import os
import sqlite3
from config import BASE_DIR

DB_PATH = BASE_DIR / "users.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(username TEXT PRIMARY KEY, salt BLOB NOT NULL, pw_hash BLOB NOT NULL)"
    )
    return conn


def _hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)


def create_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    if not username.isalnum() or not (3 <= len(username) <= 20):
        return False, "Username should be 3-20 characters long and contain only letters and numbers."
    if len(password) < 6:
        return False, "Password should be at least 6 characters long."

    salt = os.urandom(16)
    conn = _connect()
    try:
        exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if exists:
            return False, ".Username already taken. Please choose a different one."
        conn.execute(
            "INSERT INTO users (username, salt, pw_hash) VALUES (?, ?, ?)",
            (username, salt, _hash(password, salt)),
        )
        conn.commit()
    finally:
        conn.close()
    return True, "Account successfully created."


def verify_user(username: str, password: str) -> bool:
    username = username.strip().lower()
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT salt, pw_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return False
    salt, stored_hash = row
    return hmac.compare_digest(_hash(password, salt), stored_hash)