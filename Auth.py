import hashlib
import hmac
import os
import database
import session
from config import Colors

def _hash_password(password, salt_hex):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), 100_000
    ).hex()


def register():
    print("\n REGISTER")
    username = input("Username: ").strip()
    password = input("Password: ")

    if not username or not password:
        print(f"{Colors.RED} Username dan password tidak boleh kosong!{Colors.ENDC}")
        return
    if username in database.users:
        print(f"{Colors.RED} Username sudah dipakai!{Colors.ENDC}")
        return

    salt = os.urandom(16).hex()
    database.users[username] = {
        "salt": salt,
        "password_hash": _hash_password(password, salt),
    }
    database.data_user[username] = database.buat_data_baru()
    database.save()

    print(f"{Colors.GREEN} Successfully registered! {Colors.ENDC}")


def login():
    username = input("Username: ").strip()
    password = input("Password: ")
    akun = database.users.get(username)
    if akun and hmac.compare_digest(
        akun["password_hash"], _hash_password(password, akun["salt"])
    ):
        session.current_user = username
        print(f"{Colors.GREEN} Successfully logged in!{Colors.ENDC}")
        return
    print(f"{Colors.RED}Invalid username or password!{Colors.ENDC}")