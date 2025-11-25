# auth.py
import os
import hashlib
import getpass
from config import USER_FILE

def hash_value(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def ensure_user_file():
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()

def register_user() -> bool:
    ensure_user_file()
    print("\n=== Register New User ===")
    username = input("Enter new username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return False
    password = getpass.getpass("Enter new password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return False

    h_user = hash_value(username)
    h_pass = hash_value(password)

    # Check duplicates
    with open(USER_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                stored_user, _ = line.strip().split()
            except ValueError:
                continue
            if stored_user == h_user:
                print("Username already exists!")
                return False

    with open(USER_FILE, "a") as f:
        f.write(f"{h_user} {h_pass}\n")

    print("User registered successfully!\n")
    return True

def login_user() -> bool:
    ensure_user_file()
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

    h_user = hash_value(username)
    h_pass = hash_value(password)

    with open(USER_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            stored_user, stored_pass = parts[0], parts[1]
            if stored_user == h_user and stored_pass == h_pass:
                print("\nLogin successful!\n")
                return True

    print("\nInvalid username or password.\n")
    return False

def login_menu() -> bool:
    while True:
        print("=== Login Menu ===")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        ch = input("Choice: ").strip()
        if ch == "1":
            if login_user():
                return True
        elif ch == "2":
            register_user()
        elif ch == "0":
            return False
        else:
            print("Invalid choice.\n")
