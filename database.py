import json
import os
import session
from config import (DATA_DIR, USERS_FILE, DATA_USER_FILE,
                    POTONGAN_EMERGENCY_DEFAULT)


users = {}
data_user = {}


def _baca(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            isi = json.load(f)
        return isi if isinstance(isi, dict) else {}
    except (json.JSONDecodeError, OSError):
        try:
            os.replace(path, path + ".bak")
            print(f"Warning: {os.path.basename(path)} is corrupted, backed up to .bak")
        except OSError:
            pass
        return {}


def _tulis(path, isi):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(isi, f, indent=4, ensure_ascii=False)
    os.replace(tmp, path)  # atomic: file tidak setengah tertulis kalau crash


def load():
    os.makedirs(DATA_DIR, exist_ok=True)
    users.clear()
    users.update(_baca(USERS_FILE))
    data_user.clear()
    data_user.update(_baca(DATA_USER_FILE))


def save():
    os.makedirs(DATA_DIR, exist_ok=True)
    _tulis(USERS_FILE, users)
    _tulis(DATA_USER_FILE, data_user)


def buat_data_baru():
    return {
        "saldo": 0,
        "target_list": [],
        "transaksi": [],
        "histori_tabungan": [],
        "emergency_fund": 0,
        "potongan_emergency": POTONGAN_EMERGENCY_DEFAULT,
    }


def get_data():
    return data_user[session.current_user]